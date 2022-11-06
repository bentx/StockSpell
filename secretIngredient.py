import csv
import random
from datetime import datetime, timedelta
import time
import pytz
from pytz import timezone
from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn
import pymongo
from pymongo import MongoClient
import requests
from pushbullet import Pushbullet
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from csv import writer
import stockFormula
import talib
import pandas_ta as ta

def movingAverageFormula(preHigh,preLow,high,low):
    if(float(preHigh)>=float(preLow) and float(high)<=float(low) ):
        
        return True      
    return False       