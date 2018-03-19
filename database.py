# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 15:56:31 2018

@author: FSinohui
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, Query
import json

engine = create_engine('sqlite:///DataSets/belly_button_biodiversity.sqlite', convert_unicode=True, echo=False)
Base = declarative_base()
Base.metadata.reflect(engine)

class Otu(Base):
    __table__ = Base.metadata.tables['otu']


class Samples(Base):
    __table__ = Base.metadata.tables['samples']


class SamplesMetadata(Base):
    __table__ = Base.metadata.tables['samples_metadata']


session = scoped_session(sessionmaker(bind=engine))

def otuOutput():
    otuQueryReturn = session.query(Otu.lowest_taxonomic_unit_found)
    otuQueryList = [each for each in otuQueryReturn]
    otuOutputList = [each_ for (each_,) in otuQueryList]
    return otuOutputList

def washFreq(sample):
    queryExpression = session.query(SamplesMetadata.WFREQ).filter(SamplesMetadata.SAMPLEID == sample)
    washOutputList = [each_ for (each_,) in queryExpression]
    return washOutputList


def nameOutput():
    sampleNameList = [column.key for column in Samples.__table__.columns][1:]
    return sampleNameList

def metaOutput(sample):
    queryExpression = session.query(SamplesMetadata.AGE, SamplesMetadata.BBTYPE, SamplesMetadata.ETHNICITY, 
                                    SamplesMetadata.GENDER, SamplesMetadata.LOCATION, 
                                    SamplesMetadata.SAMPLEID).filter(SamplesMetadata.SAMPLEID == sample)
    dataDict = [{"age": each[0],
                 "BBTYPE": each[1],
                 'GENDER': each[3],
                 'ETHNICITY': each[2],
                 'LOCATION': each[4],
                 'SAMPLEID': each[5]
                 } for each in queryExpression]

    return dataDict


def sampleJson(sample):
    query = 'SELECT otu_id, %s FROM Samples ORDER BY %s DESC LIMIT 10' % (sample, sample)
    queryData = engine.execute(query)
    queryList = [each for each in queryData]
    otu_id, sampleValues = zip(*queryList)
    dataDict = {"otu_ids": list(otu_id),
                "sample_values": list(sampleValues)
                }
    return dataDict

def sampleJsonAll(sample):
    query = 'SELECT otu_id, %s FROM Samples ORDER BY %s DESC LIMIT 100' % (sample, sample)
    queryData = engine.execute(query)
    queryList = [each for each in queryData]
    otu_id, sampleValues = zip(*queryList)
    dataDict = {"otu_ids": list(otu_id),
                "sample_values": list(sampleValues)
                }
    return dataDict