#!/bin/sh

thrift --gen py -out ./ ./idl/*.thrift

python type_generator.py