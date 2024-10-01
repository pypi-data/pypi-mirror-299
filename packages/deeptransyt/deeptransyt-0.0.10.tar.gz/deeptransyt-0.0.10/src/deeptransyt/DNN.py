import torch
import torch.nn as nn
import pytorch_lightning as pl
import torchmetrics
from torch.optim.lr_scheduler import ReduceLROnPlateau
from torchmetrics.classification import BinaryAccuracy


class DNN(pl.LightningModule):
    def __init__(self, num_classes):
        super(DNN, self).__init__()

        self.fc1 = nn.Linear(1280, 946)
        self.bn1 = nn.BatchNorm1d(946)
        self.dropout1 = nn.Dropout(0.233)
        
        self.fc2 = nn.Linear(946, 592)
        self.bn2 = nn.BatchNorm1d(592)
        self.dropout2 = nn.Dropout(0.233)
        
        self.fc3 = nn.Linear(592, 341)
        self.bn3 = nn.BatchNorm1d(341)
        self.dropout3 = nn.Dropout(0.233)
        
        self.fc4 = nn.Linear(341, num_classes)
        
        self.criterion = nn.CrossEntropyLoss()
        self.accuracy = torchmetrics.Accuracy("multiclass", num_classes=num_classes) 
    
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.bn1(x)
        x = self.dropout1(x)

        x = torch.relu(self.fc2(x))
        x = self.bn2(x)
        x = self.dropout2(x)

        x = torch.relu(self.fc3(x))
        x = self.bn3(x)
        x = self.dropout3(x)

        x = self.fc4(x)  
        return x

    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = self.criterion(y_hat, y)
        acc = self.accuracy(y_hat, y)
        self.log('train_loss', loss, on_step=False, on_epoch=True, prog_bar=True)
        self.log('train_acc', acc, on_step=False, on_epoch=True, prog_bar=True)
        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = self.criterion(y_hat, y)
        acc = self.accuracy(y_hat, y)
        self.log('val_loss', loss, on_epoch=True, prog_bar=True)
        self.log('val_acc', acc, on_epoch=True, prog_bar=True)
        return {'val_loss': loss, 'val_acc': acc}

    def test_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = self.criterion(y_hat, y)
        acc = self.accuracy(y_hat, y)
        self.log('test_loss', loss)
        self.log('test_acc', acc)
        return {'test_loss': loss, 'test_acc': acc}

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=0.001)
        lr_scheduler = {'scheduler': ReduceLROnPlateau(optimizer, mode='min', factor=0.1, patience=5, verbose=True),
                        'monitor': 'val_loss',  
                        'reduce_on_plateau': True}
        return [optimizer], [lr_scheduler]
    


class DNN_binary(pl.LightningModule):
    def __init__(self):
        super(DNN_binary, self).__init__()

        self.fc1 = nn.Linear(1280, 946)
        self.bn1 = nn.BatchNorm1d(946)
        self.dropout1 = nn.Dropout(0.233)
        
        self.fc2 = nn.Linear(946, 592)
        self.bn2 = nn.BatchNorm1d(592)
        self.dropout2 = nn.Dropout(0.233)
        
        self.fc3 = nn.Linear(592, 341)
        self.bn3 = nn.BatchNorm1d(341)
        self.dropout3 = nn.Dropout(0.233)
        
        self.fc4 = nn.Linear(341, 1)
        
        self.criterion = nn.BCEWithLogitsLoss()
        self.accuracy = BinaryAccuracy()

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.bn1(x)
        x = self.dropout1(x)

        x = torch.relu(self.fc2(x))
        x = self.bn2(x)
        x = self.dropout2(x)

        x = torch.relu(self.fc3(x))
        x = self.bn3(x)
        x = self.dropout3(x)

        x = self.fc4(x)  
        return x

    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x).squeeze()
        loss = self.criterion(y_hat, y.float())
        acc = self.accuracy(torch.sigmoid(y_hat), y)
        self.log('train_loss', loss, on_step=False, on_epoch=True, prog_bar=True)
        self.log('train_acc', acc, on_step=False, on_epoch=True, prog_bar=True)
        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x).squeeze()
        loss = self.criterion(y_hat, y.float())
        acc = self.accuracy(torch.sigmoid(y_hat), y)
        self.log('val_loss', loss, on_epoch=True, prog_bar=True)
        self.log('val_acc', acc, on_epoch=True, prog_bar=True)
        return {'val_loss': loss, 'val_acc': acc}

    def test_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x).squeeze()
        loss = self.criterion(y_hat, y.float())
        acc = self.accuracy(torch.sigmoid(y_hat), y)
        self.log('test_loss', loss)
        self.log('test_acc', acc)
        return {'test_loss': loss, 'test_acc': acc}

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=0.001)
        lr_scheduler = {'scheduler': ReduceLROnPlateau(optimizer, mode='min', factor=0.1, patience=5, verbose=True),
                        'monitor': 'val_loss',  
                        'reduce_on_plateau': True}
        return [optimizer], [lr_scheduler]
    

class DNN_weight(pl.LightningModule):
    def __init__(self, num_classes, weight):
        super(DNN_weight, self).__init__()

        self.fc1 = nn.Linear(1280, 946)
        self.bn1 = nn.BatchNorm1d(946)
        self.dropout1 = nn.Dropout(0.233)
        
        self.fc2 = nn.Linear(946, 592)
        self.bn2 = nn.BatchNorm1d(592)
        self.dropout2 = nn.Dropout(0.233)
        
        self.fc3 = nn.Linear(592, 341)
        self.bn3 = nn.BatchNorm1d(341)
        self.dropout3 = nn.Dropout(0.233)
        
        self.fc4 = nn.Linear(341, num_classes)
        
        self.criterion = nn.CrossEntropyLoss(weight=weight)
        self.accuracy = torchmetrics.Accuracy("multiclass", num_classes=num_classes) 

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.bn1(x)
        x = self.dropout1(x)

        x = torch.relu(self.fc2(x))
        x = self.bn2(x)
        x = self.dropout2(x)

        x = torch.relu(self.fc3(x))
        x = self.bn3(x)
        x = self.dropout3(x)

        x = self.fc4(x)  
        return x

    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = self.criterion(y_hat, y)
        acc = self.accuracy(y_hat, y)
        self.log('train_loss', loss, on_step=False, on_epoch=True, prog_bar=True)
        self.log('train_acc', acc, on_step=False, on_epoch=True, prog_bar=True)
        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = self.criterion(y_hat, y)
        acc = self.accuracy(y_hat, y)
        self.log('val_loss', loss, on_epoch=True, prog_bar=True)
        self.log('val_acc', acc, on_epoch=True, prog_bar=True)
        return {'val_loss': loss, 'val_acc': acc}

    def test_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = self.criterion(y_hat, y)
        acc = self.accuracy(y_hat, y)
        self.log('test_loss', loss)
        self.log('test_acc', acc)
        return {'test_loss': loss, 'test_acc': acc}

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=0.001)
        lr_scheduler = {'scheduler': ReduceLROnPlateau(optimizer, mode='min', factor=0.1, patience=5, verbose=True),
                        'monitor': 'val_loss',  
                        'reduce_on_plateau': True}
        return [optimizer], [lr_scheduler]
    
class HierarchicalDNN(pl.LightningModule):
    def __init__(self, input_size, num_families, num_subfamilies):
        super(HierarchicalDNN, self).__init__()

        self.fc1 = nn.Linear(input_size, 1024)
        self.bn1 = nn.BatchNorm1d(1024)
        self.dropout1 = nn.Dropout(0.3)
        
        self.fc2 = nn.Linear(1024, 640)
        self.bn2 = nn.BatchNorm1d(640)
        self.dropout2 = nn.Dropout(0.3)
        
        self.fc3 = nn.Linear(640, 230)
        self.bn3 = nn.BatchNorm1d(230)
        self.dropout3 = nn.Dropout(0.3)
        
        self.fc_family = nn.Linear(230, num_families)
        self.fc_subfamily = nn.Linear(230, num_subfamilies)
        
        self.criterion = nn.CrossEntropyLoss()
        self.family_accuracy = torchmetrics.Accuracy("multiclass", num_classes=num_families)
        self.subfamily_accuracy = torchmetrics.Accuracy("multiclass", num_classes=num_subfamilies)
    
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.bn1(x)
        x = self.dropout1(x)

        x = torch.relu(self.fc2(x))
        x = self.bn2(x)
        x = self.dropout2(x)

        x = torch.relu(self.fc3(x))
        x = self.bn3(x)
        x = self.dropout3(x)

        family_output = self.fc_family(x)
        subfamily_output = self.fc_subfamily(x)
        return family_output, subfamily_output

    def training_step(self, batch, batch_idx):
        x, y_fam, y_sub = batch
        fam_output, sub_output = self(x)
        
        loss_fam = self.criterion(fam_output, y_fam)
        loss_sub = self.criterion(sub_output, y_sub)
        loss = loss_fam + loss_sub

        fam_acc = self.family_accuracy(fam_output, y_fam)
        sub_acc = self.subfamily_accuracy(sub_output, y_sub)
        
        self.log('train_loss', loss, on_step=False, on_epoch=True, prog_bar=True)
        self.log('train_fam_acc', fam_acc, on_step=False, on_epoch=True, prog_bar=True)
        self.log('train_sub_acc', sub_acc, on_step=False, on_epoch=True, prog_bar=True)
        return loss
    
    def test_step(self, batch, batch_idx):
        x, y_fam, y_sub = batch
        fam_output, sub_output = self(x)

        loss_fam = self.criterion(fam_output, y_fam)
        loss_sub = self.criterion(sub_output, y_sub)
        loss = loss_fam + loss_sub

        fam_acc = self.family_accuracy(fam_output, y_fam)
        sub_acc = self.subfamily_accuracy(sub_output, y_sub)
        
        self.log('test_loss', loss, on_step=False, on_epoch=True, prog_bar=True)
        self.log('test_fam_acc', fam_acc, on_step=False, on_epoch=True, prog_bar=True)
        self.log('test_sub_acc', sub_acc, on_step=False, on_epoch=True, prog_bar=True)
        return loss

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=0.001)
        lr_scheduler = {'scheduler': ReduceLROnPlateau(optimizer, mode='min', factor=0.1, patience=5, verbose=True),
                        'monitor': 'train_loss',  
                        'reduce_on_plateau': True}
        return [optimizer], [lr_scheduler]
