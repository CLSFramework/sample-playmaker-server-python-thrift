#!/bin/sh

thrift --gen py -out ./ ./idl/*.thrift

python3 type_generator.py