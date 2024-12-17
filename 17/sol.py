import re
import sys
from collections import defaultdict

ADV = 0
BXL = 1
BST = 2
JNZ = 3
BXC = 4
OUT = 5
BDV = 6
CDV = 7
OP_LIT0 = 0
OP_LIT1 = 1
OP_LIT2 = 2
OP_LIT3 = 3
OP_REGA = 4
OP_REGB = 5
OP_REGC = 6
OP_INVAL = 7
REG_A = 0
REG_B = 1
REG_C = 2
DEBUG = False

def fatal_error(message):
    print(message, file=sys.stderr)
    raise

def get_operand_value(registers, operand, literal=False):
    if literal:
        if operand in range(8):
            return operand
        fatal_error(f'unknown operand {operand}')

    if operand in [OP_LIT0, OP_LIT1, OP_LIT2, OP_LIT3]:
        return operand
    if operand == OP_REGA:
        return registers[REG_A]
    if operand == OP_REGB:
        return registers[REG_B]
    if operand == OP_REGC:
        return registers[REG_C]
    fatal_error(f'operand {operand} invalid')

def do_adv(registers, operand, ip):
    if DEBUG:
        print(f'ADV: {operand}')
        print(f'A: {registers[REG_A]} -> {registers[REG_A] // (2 ** get_operand_value(registers, operand))}')
    registers[REG_A] = \
        registers[REG_A] // (2 ** get_operand_value(registers, operand))
    return ip + 2

def do_bxl(registers, operand, ip):
    if DEBUG:
        print(f'BXL: {operand}')
        print(f'B: {registers[REG_B]} -> {registers[REG_B] ^ get_operand_value(registers, operand, True)}')
    registers[REG_B] = \
        registers[REG_B] ^ get_operand_value(registers, operand, True)
    return ip + 2

def do_bst(registers, operand, ip):
    if DEBUG:
        print(f'BST: {operand}')
        print(f'B: {registers[REG_B]} -> {get_operand_value(registers, operand) % 8}')
    registers[REG_B] = \
        get_operand_value(registers, operand) % 8
    return ip + 2

def do_jnz(registers, operand, ip):
    if DEBUG:
        print(f'JNZ: {operand}')
        print(f'IP: {ip} -> {ip + 2 if registers[REG_A] == 0 else get_operand_value(registers, operand, True)}')
    if registers[REG_A] == 0: return ip + 2
    return get_operand_value(registers, operand, True)

def do_bxc(registers, ip):
    if DEBUG:
        print('BXC')
        print(f'B: {registers[REG_B]} -> {registers[REG_B] ^ registers[REG_C]}')
    registers[REG_B] = \
        registers[REG_B] ^ registers[REG_C]
    return ip + 2

def do_out(registers, operand, ip, output):
    if DEBUG:
        print(f'OUT: {operand}')
        print(f'OUTPUT: {output} -> {output + [get_operand_value(registers, operand) % 8]}')
    output.append(get_operand_value(registers, operand) % 8)
    return ip + 2

def do_bdv(registers, operand, ip):
    if DEBUG:
        print(f'BDV: {operand}')
        print(f'B: {registers[REG_B]} -> {registers[REG_A] // (2 ** get_operand_value(registers, operand))}')
    registers[REG_B] = \
        registers[REG_A] // (2 ** get_operand_value(registers, operand))
    return ip + 2

def do_cdv(registers, operand, ip):
    if DEBUG:
        print(f'CDV: {operand}')
        print(f'C: {registers[REG_C]} -> {registers[REG_A] // (2 ** get_operand_value(registers, operand))}')
    registers[REG_C] = \
        registers[REG_A] // (2 ** get_operand_value(registers, operand))
    return ip + 2

def run_instruction(registers, output, instructions, ip):
    opcode, operand = instructions[ip], instructions[ip + 1]
    if opcode == ADV: return do_adv(registers, operand, ip)
    if opcode == BXL: return do_bxl(registers, operand, ip)
    if opcode == BST: return do_bst(registers, operand, ip)
    if opcode == JNZ: return do_jnz(registers, operand, ip)
    if opcode == BXC: return do_bxc(registers, ip)
    if opcode == OUT: return do_out(registers, operand, ip, output)
    if opcode == BDV: return do_bdv(registers, operand, ip)
    if opcode == CDV: return do_cdv(registers, operand, ip)
    fatal_error(f'unknown opcode {opcode}')

def run_program(init_a, instructions):
    registers[REG_A] = init_a
    registers[REG_B] = 0
    registers[REG_C] = 0
    output = []
    ip = 0

    while True:
        ip = run_instruction(registers, output, instructions, ip)
        if DEBUG:
            print(ip, registers, output)
        if ip >= len(instructions): break
    
    return output

with open("input.txt") as file:
    lines = file.read().strip().split("\n")
    registers = list(map(int, re.findall(r'\d+', ''.join(lines[:3]))))
    instructions = list(map(int, re.findall(r'\d+', ''.join(lines[3:]))))
    output = []
    ip = 0

    while True:
        ip = run_instruction(registers, output, instructions, ip)
        if DEBUG:
            print(ip, registers, output)
        if ip >= len(instructions): break

    print(''.join(map(str, output)))
    

    tried = set()
    power = 0
    correct_input = 0
    i = len(instructions) - 1

    while i >= 0:
        required_digit = instructions[i]
        for offset in range(8):
            if (correct_input + offset, power) in tried:
                continue

            output = run_program(correct_input + offset, instructions)
            if output[0] == required_digit:
                tried.add((correct_input + offset, power))
                correct_input += offset
                correct_input *= 8
                power += 1
                i -= 1
                break
        
        else:
            power -= 1
            correct_input //= 8
            correct_input -= correct_input % 8
            i += 1
    
    correct_input //= 8
    
    print(correct_input)