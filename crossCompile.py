import argparse
import json

def decodeInstruction(tokens, instructionNameMappingsDictionary, registerConstantMappingsDictionary):
    parseType = instructionNameMappingsDictionary[tokens[0]]["parseType"]
    # Opcode
    opcodeBin = instructionNameMappingsDictionary[tokens[0]]["opcode"]
    # Funct
    functBin = instructionNameMappingsDictionary[tokens[0]]["funct"]

    if (parseType == "aluInstruction") or (parseType == "shiftInstructionReg"):
        # rs
        rdDec = registerConstantMappingsDictionary[tokens[1].translate( { ord(","): None } )]
        rdBin = format(int(rsDec, 10), "005b")
        # rt
        rsDec = registerConstantMappingsDictionary[tokens[2].translate( { ord(","): None } )]
        rsBin = format(int(rtDec, 10), "005b")
        # rd
        rtDec = registerConstantMappingsDictionary[tokens[3].translate( { ord(","): None } )]
        rtBin = format(int(rdDec, 10), "005b")
        # shamt
        shamtBin = format(int("0", 2), "005b")
    elif parseType == "shiftInstructionConst":
        # rs
        rsBin = format(int("0", 2), "005b")
        # rt
        rtDec = registerConstantMappingsDictionary[tokens[1].translate( { ord(","): None } )]
        rtBin = format(int(rtDec, 10), "005b")
        # rd
        rdDec = registerConstantMappingsDictionary[tokens[2].translate({ord(","): None})]
        rdBin = format(int(rdDec, 10), "005b")
        # shamt
        shamtDec = tokens[3].translate({ord(","): None})
        shamtBin = format(int(shamtDec, 10), "005b")
    elif parseType == "mulDivMfInstruction":
        # rs
        rsBin = format(int("0", 2), "005b")
        # rt
        rtBin = format(int("0", 2), "005b")
        # rd
        rdDec = registerConstantMappingsDictionary[tokens[1].translate({ord(","): None})]
        rdBin = format(int(rdDec, 10), "005b")
        # shamt
        shamtBin = format(int("0", 2), "005b")
    elif parseType == "mulDivMtInstruction":
        # rs
        rsDec = registerConstantMappingsDictionary[tokens[1].translate({ord(","): None})]
        rsBin = format(int(rsDec, 10), "005b")
        # rt
        rtBin = format(int("0", 2), "005b")
        # rd
        rdBin = format(int("0", 2), "005b")
        # shamt
        shamtBin = format(int("0", 2), "005b")
    elif parseType == "mulDivInstruction":
        # rs
        rsDec = registerConstantMappingsDictionary[tokens[1].translate({ord(","): None})]
        rsBin = format(int(rsDec, 10), "005b")
        # rt
        rtDec = registerConstantMappingsDictionary[tokens[2].translate({ord(","): None})]
        rtBin = format(int(rtDec, 10), "005b")
        # rd
        rdBin = format(int("0", 2), "005b")
        # shamt
        shamtBin = format(int("0", 2), "005b")
    else:
        raise Exception("Error: Could not parse the instruction correctly.")

    instructionBinaryString = opcodeBin + rsBin + rtBin + rdBin + shamtBin + functBin
    return format(int(instructionBinaryString, 2), "008x")

def main(args):
    instructionNameMappingsFilename = "./instructionNameMappings.json"
    registerConstantMappingsFilename = "./registerConstantMappings.json"

    try:
        with open(instructionNameMappingsFilename, 'r') as f:
            instructionNameMappingsDictionary = json.load(f)
    except Exception as ex:
        print(f"Could not load '{instructionNameMappingsFilename}'. Aborting...")
        return
    try:
        with open(registerConstantMappingsFilename, 'r') as f:
            registerConstantMappingsDictionary = json.load(f)
    except Exception as ex:
        print(f"Could not load '{registerConstantMappingsFilename}'. Aborting...")
        return

    inputFile = open(args.inputFile, "r")
    outputFile = open(args.outputFile, "w")

    for line in inputFile:
        tokens = line.split()
        decodedInstructionHex = decodeInstruction(
            tokens,
            instructionNameMappingsDictionary,
            registerConstantMappingsDictionary
        )
        outputFile.write(f"{decodedInstructionHex}\n")

    inputFile.close()
    outputFile.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("inputFile", type=str, help="")
    parser.add_argument("outputFile", type=str, help="")
    args = parser.parse_args()
    main(args)
