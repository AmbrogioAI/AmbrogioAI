import utilities.getClasses as getClasses
import random
import os
import numpy as np
from torchvision import transforms
# Crea i DataLoader per training e validazione
from torch.utils.data import DataLoader
from utilities.ImageTransformer import CustomImageDataset
from classes.TestingMode import TestingMode

class DataSetManager:
    def __init__(self):
        self.imagesPath = "DataSet/"
        self.jsonPath = "DataSet\dataSet.json"

    def getTestSetPaths(self):
        casualTest = [
            "20241004111232.jpg",
            "20241004140513.jpg",
            "c1.png",
            "c2.png",
            "c4.png",
            "ca.jpg",
            "20241004110822.jpg",
            "casua.jpg",
            "c5.png",
            "20240927095059.jpg",
            "20241004110806.jpg",
            "c3.png",
            "20240927095048.jpg",
            "20241004111308.jpg",
        ]
        eleganteTest = [
            "20240927101537.jpg",
            "20240927101540.jpg",
            "20240927101606.jpg",
            "20241002133018.jpg",
            "20241004110752.jpg",
            "20241004110758.jpg",
            "20241004111318.jpg",
            "e1.png",
            "e2.png",
            "e3.png",
            "e4.png",
            "e5.png",
            "e6.png",
            "elegan.jpg",           
        ]
        sportivoTest = [
            "20240927095051.jpg",
            "20240927101531.jpg",
            "20241004140523.jpg",
            "s.jpg",
            "s1.png",
            "s2.png",
            "s3.png",
            "sp.jpg",
            "spo.jpg",
            "spor.jpg",
            "sport.jpg",
            "sporti.jpg",
            "sportiv.jpg",
            "sportivo.jpg",        
        ]

        casualTest = [self.imagesPath + "casual/" + i for i in casualTest]
        eleganteTest = [self.imagesPath + "elegante/" + i for i in eleganteTest]
        sportivoTest = [self.imagesPath + "sportivo/" + i for i in sportivoTest]

        return casualTest, eleganteTest, sportivoTest
    
    def getAllImages(self):
        '''
        get the entire dataset in a form of a list of image paths in ORDER 
        '''
        # get all the images from the DataSet folder
        classes = getClasses.getClasses()
        images = []
        for c in classes:
            pathChosen = self.imagesPath + c + "/"
            images += [pathChosen + i for i in os.listdir(pathChosen)]
        
        for i,path in enumerate(images):
            # check if in path is contained .DS_Store
            if ".DS_Store" in path:
                images.pop(i)
        
        return images
    
    def getCorrentPredictionOfImage(self,imagePath):
        '''
        given the path of the image, return the correct prediction of the image that ambrogio should return
        '''
        # get the correct prediction of the image
        classes = getClasses.getClasses()
        for c in classes:
            if c in imagePath:
                toRet = [0 for x in range(len(classes))]
                toRet[classes.index(c)] = 1
                return toRet
        return None
    
    def getRandomImage(self):
        '''
        get a random image path of the dataset
        '''
        # go in the DataSet folder and get a random image from a random class
        classes = getClasses.getClasses()
        randomClass = random.choice(classes)
        pathChosen = self.imagesPath + randomClass + "/"
        images = os.listdir(pathChosen)
        
        return pathChosen + random.choice(images)        
    
    def partitionDataSet(self):
        '''
        The data will be a tuple
        return 0 => the training set, 1 => the convalidation 
        '''
        # partition the data set into training and test set
        images = self.getAllImages()
        random.shuffle(images)
        trainingSet = images[:int(len(images)*0.7)]
        convalidationSet = images[int(len(images)*0.7):]
        
        
        return trainingSet,convalidationSet
    
    def randomShuffleDataSet(self):
        '''
        get all the data set like 'getAllImages' but shuffled randomly
        '''
        # shuffle the dataset
        images = self.getAllImages()
        random.shuffle(images)
        return images
    
    def convertPassedTargetsToTrainingTargets(self,targets: list):
        '''
        convert the passed targets to the training targets
        exaple: [ [ 0 , 1 , 0 ] , [ 1 , 0 , 0 ] , [ 0 , 0 , 1 ] ] => [ 1 , 0 , 2 ]
        
        :param targets: the targets to convert
        :return: the converted targets
        '''
        # convert the passed targets to the training targets
        for i in range(len(targets)):
            targets[i] = targets[i].index(1)
        return targets
    
    def partitionDataSetRandomly(self,percTraining=0.7,percValidation=0.2):
        '''
        partition the dataset into training, validation and test set
        '''
        # partition the dataset into training, validation and test set
        images = self.getAllImages()
        random.shuffle(images)

        train_end = int(len(images) * percTraining)
        val_end = train_end + int(len(images) * percValidation)

        trainingSet = images[:train_end]
        validationSet = images[train_end:val_end]
        testSet = images[val_end:]

        return trainingSet,validationSet,testSet
    
    def partitionDataSetEqualy(self,percTraining=0.7,percValidation=0.3):
        '''
        partition the dataset into training, validation and test set equaly for each class
        '''
        
        casualTest, eleganteTest, sportivoTest = self.getTestSetPaths()
        testSet = casualTest + eleganteTest + sportivoTest

        # partition the dataset into training, validation and test set
        images = self.getAllImages()
        images = [i for i in images if i not in testSet]
        imagesWithClass = []
        for i,img in enumerate(images):
            target = self.getCorrentPredictionOfImage(img)
            imagesWithClass.append({"img":img,"target":self.resolveTarget(target)})
        
        casual = []
        elegante = []
        sport = []
        
        
        for i in imagesWithClass:
            if i["target"] == "casual":
                casual.append(i["img"])
            elif i["target"] == "elegante":
                elegante.append(i["img"])
            elif i["target"] == "sportivo":
                sport.append(i["img"])
        
        minLen = min(len(casual),len(elegante),len(sport))
        percMin = minLen*percTraining
        
        TrainingSet = casual[:int(percMin)] + elegante[:int(percMin)] + sport[:int(percMin)]
        ValidationSet = casual[int(percMin):int(percMin+minLen*percValidation)] + elegante[int(percMin):int(percMin+minLen*percValidation)] + sport[int(percMin):int(percMin+minLen*percValidation)]
        
        return TrainingSet,ValidationSet,testSet
        
    def resolveTarget(self,target):
        '''
        resolve the target to the class
        '''
        # resolve the target to the class
        classes = getClasses.getClasses()
        return classes[target.index(1)]
    
    
    def getSetForRes50(self,mode = TestingMode.TestWithRealImages):
        # Ottieni i dataset
        
        trainingSet, validationSet, testSet = [[] for _ in range(3)]

        if mode == TestingMode.TestWithRealImages:
            trainingSet, validationSet, testSet = self.partitionDataSetEqualy()
        elif mode == TestingMode.TestWithRandomImages:
            trainingSet, validationSet, testSet = self.partitionDataSetRandomly()

        # Funzione di trasformazione delle immagini

        data_transforms = {
            'train': transforms.Compose([
                transforms.Resize(256),
                transforms.RandomResizedCrop(224),
                transforms.RandomHorizontalFlip(),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            ]),
            'val': transforms.Compose([
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            ]),
            'test': transforms.Compose([
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            ])
        }

        # Crea i dataset personalizzati per training e validazione
        train_dataset = CustomImageDataset(trainingSet, transform=data_transforms['train'], target_func=self.getCorrentPredictionOfImage)
        val_dataset = CustomImageDataset(validationSet, transform=data_transforms['val'], target_func=self.getCorrentPredictionOfImage)
        test_dataset = CustomImageDataset(testSet, transform=data_transforms['test'], target_func=self.getCorrentPredictionOfImage)
        

        train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True, num_workers=4)
        val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False, num_workers=4)
        test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False, num_workers=4)

        dataloaders = {
            'train': train_loader,
            'val': val_loader,
            'test': test_loader
        }
        dataset_sizes = {
            'train': len(train_dataset), 
            'val': len(val_dataset),
            'test': len(test_dataset)
        }
        return dataloaders, dataset_sizes
    

