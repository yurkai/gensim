#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 Loreto Parisi <loretoparisi@gmail.com>
# Copyright (C) 2016 Silvio Olivastri <silvio.olivastri@gmail.com>
# Copyright (C) 2016 Radim Rehurek <radim@rare-technologies.com>


"""This script helps to convert data in word2vec format to Tensorflow 2D tensor
and metadata formats for Embedding Visualization.

To use the generated TSV 2D tensor and metadata file in the Projector 
Visualizer, please follow next steps:
1) Open http://projector.tensorflow.org/
2) Choose "Load Data" from the left menu.
3) Select "Choose file" in "Load a TSV file of vectors." and choose you local 
"_tensor.tsv" file.
4) Select "Choose file" in "Load a TSV file of metadata." and choose you local 
"_metadata.tsv" file.

For more information about TensorBoard TSV format please visit:
https://www.tensorflow.org/versions/master/how_tos/embedding_viz/

Usage
-----
python -m gensim.scripts.word2vec2tensor --input <Word2Vec_model_file> --output <TSV_tensor_filename_prefix> [--binary] <Word2Vec_binary_flag>

Parameters
----------
Word2Vec_model_file
    Input Word2Vec file.

TSV_tensor_filename_prefix
    Prefix for produced files.

Word2Vec_binary_flag, optional
    Use True if provided Word2Vec in binary format.

Produces
--------
TENSOR_PREFIX_tensor.tsv
    2D tensor file.
TENSOR_PREFIX_metadata.tsv
    Word Embedding metadata file.

Example
-------
python -m gensim.scripts.word2vec2tensor --input my_w2v.txt --output visual

"""

import os
import sys
import logging
import argparse

import gensim

logger = logging.getLogger(__name__)


def word2vec2tensor(word2vec_model_path, tensor_filename, binary=False):
    """Converts Word2Vec model and writes two files 2D tensor TSV file (ends 
    with _tensor.tsv) and metadata file (ends with _metadata.tsv).

    Parameters
    ----------
    word2vec_model_path : str
        Path to input Word2Vec file.
    tensor_filename : str 
        Prefix for output files. 
    binary : bool, optional
        True if input file in binary format.

    """
    model = gensim.models.KeyedVectors.load_word2vec_format(word2vec_model_path, binary=binary)
    outfiletsv = tensor_filename + '_tensor.tsv'
    outfiletsvmeta = tensor_filename + '_metadata.tsv'

    with open(outfiletsv, 'w+') as file_vector:
        with open(outfiletsvmeta, 'w+') as file_metadata:
            for word in model.index2word:
                file_metadata.write(gensim.utils.to_utf8(word) + gensim.utils.to_utf8('\n'))
                vector_row = '\t'.join(str(x) for x in model[word])
                file_vector.write(vector_row + '\n')

    logger.info("2D tensor file saved to %s", outfiletsv)
    logger.info("Tensor metadata file saved to %s", outfiletsvmeta)


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s : %(threadName)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s", ' '.join(sys.argv))

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, help="Input word2vec model")
    parser.add_argument("-o", "--output", required=True, help="Output tensor file name prefix")
    parser.add_argument(
        "-b", "--binary", required=False, help="If word2vec model in binary format, set True, else False"
    )
    args = parser.parse_args()

    word2vec2tensor(args.input, args.output, args.binary)

    logger.info("finished running %s", os.path.basename(sys.argv[0]))
