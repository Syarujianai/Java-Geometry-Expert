import os
import re
import cv2
import json
import ipdb
from geosolver.diagram.parse_image_segments import parse_image_segments
from geosolver.diagram.parse_primitives import parse_primitives
from geosolver.diagram.select_primitives import select_primitives
from geosolver.diagram.parse_core import parse_core
from geosolver.diagram.parse_graph import parse_graph
from geosolver.diagram.get_instances import get_all_instances

from jpype import *
from try2 import GeometryImageParser

startJVM(getDefaultJVMPath(), "-ea",
        "-Djava.class.path=C:/Users/DM/Desktop/code/geo/Java-Geometry-Expert/out/artifacts/Java_Geometry_Expert_jar2/Java-Geometry-Expert.jar;"
        "-Djava.ext.dirs = C:/Users/DM/Desktop/code/geo/Java-Geometry-Expert/dependency", 
        "-Xms1g","-Xmx1g")
Main2 = JClass('gprover.Main2')

def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

def test_prover(problem_id):
    dir_path = "C:/Users/DM/Desktop/Junior Mathematics/"
    text_path = dir_path+"example_{}.txt".format(problem_id)
    diagram_path = dir_path+"example_{}.JPG".format(problem_id)
    positions_path = dir_path+"positions_{}.txt".format(problem_id)

    # parse the positions of image by geosolver
    gimg_parser = GeometryImageParser()
    ret = gimg_parser.parse_image(diagram_path)
    if not os.path.exists(positions_path):   
        try:
            with open(positions_path, "w") as f:      
                f.write(ret)
        except IOError as error:
            print(error)
    
    # prove the example by JGEX
    proof = Main2.parse_and_prove_problem(problem_id, 1)  # problem_id, out_mode
    print(proof)
    proof_steps = proof.strip().split("\n")
    for step in proof_steps:
        step_filtered = re.sub(r"(\(.*?\))", '', step)
        symbols = re.findall(r"([A-Z]+(?:[A-Z]+)+)", step_filtered)
        tuple_symbols = [tuple([s for s in symbol.encode("raw_unicode_escape")]) for symbol in symbols]
        print(step)
        if step.encode("raw_unicode_escape").find("\u2220") >= 0:
            gimg_parser.display_instances("angle", tuple_symbols)
        elif step.find("tri") >= 0:
            gimg_parser.display_instances("polygon", tuple_symbols)
        else:
            gimg_parser.display_instances("line", tuple_symbols)
        

if __name__ == "__main__":
    test_prover(3)