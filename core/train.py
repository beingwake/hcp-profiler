import logging

import torch
from datetime import datetime
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter

from utils.dataset import train_val_dataset, ServerLogDataset
from utils.model import NeuralNetwork



def train_one_epoch(epoch_index, tb_writer):
    running_loss = 0
    last_loss = 0

    for i, data in enumerate(dataloaders["train"]):
        inputs, labels = data
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = loss_fn(outputs, labels.float())
        loss.backward()

        optimizer.step()

        running_loss += loss.item()

        if(i % 1000 == 999):
            last_loss = running_loss/1000 # loss per batch
            print('batch {} loss: {}'.format(i+1, last_loss))
            tb_x = epoch_index * len(dataloaders["train"]) + i + 1
            tb_writer.add_scalar('Loss/train', last_loss, tb_x)
            running_loss = 0.
    return last_loss

if __name__=="__main__":

    # logging.warn("Training data is preparing...")

    dataset = ServerLogDataset("/home/coco/hcp/hcp-profiler/experiments/data-processed/model-train-test.csv")
    datasets = train_val_dataset(dataset)

    dataloaders = {x: DataLoader(datasets[x], batch_size=8, shuffle=True) for x in ["train", "val"]}

   
    model = NeuralNetwork()

    loss_fn = torch.nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)


    timestamp = datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
    writer = SummaryWriter('runs/profier_{}'.format(timestamp))
    epoch_number = 0
    EPOCHS = 100
    
    best_vloss = 1_000_000.

    for epoch in range(EPOCHS):
        print('EPOCH {}'.format(epoch_number + 1))
        model.train(True)
        avg_loss = train_one_epoch(epoch_number, writer)

        running_vloss = 0.0

        model.eval()

        with torch.no_grad():
            for i, vdata in enumerate(dataloaders["val"]):
                vinputs, vlabels = vdata
                voutputs = model(vinputs)
                vloss = loss_fn(voutputs, vlabels)
                running_vloss += vloss

        avg_vloss = running_vloss / (i+1)
        print('LOSS train {} valid {}'.format(avg_loss, avg_vloss))

        writer.add_scalars('Training vs. Validation Loss',
                           { 'Training' : avg_loss, 'Validation': avg_vloss},
                           epoch_number + 1)
        
        writer.flush()

        if avg_vloss < best_vloss:
            best_vloss = avg_vloss
            # model_path = 'model_{}_{}'.format(timestamp, epoch_number) + ".pth"
            torch.save(model.state_dict(), "experiments/models/model_{}.pth".format(epoch_number))
            print("model_{}.pth saved".format(epoch_number))

        epoch_number += 1
