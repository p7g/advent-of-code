from aoc import *

T_SUM = 0
T_PRODUCT = 1
T_MIN = 2
T_MAX = 3
T_LITERAL = 4
T_GT = 5
T_LT = 6
T_EQ = 7

LT_TOTAL_BITS = 0
LT_NUM_PACKETS = 1

Packet = namedtuple("Packet", "version,type,value,subpackets")


def _decode_packet(bits):
    header, payload = bits[:6], bits[6:]
    version, type_id = int(header[:3], 2), int(header[3:], 2)

    if type_id == T_LITERAL:
        num_bits = []
        pos = 0
        for pos in range(0, len(payload), 5):
            more, part = payload[pos] == "1", payload[pos + 1 : pos + 5]
            num_bits += part
            if not more:
                break
        return (
            Packet(version, T_LITERAL, int("".join(num_bits), 2), None),
            payload[pos + 5:],
        )

    length_type_id, payload = int(payload[0], 2), payload[1:]
    if length_type_id == LT_TOTAL_BITS:
        total_bits, payload = int(payload[:15], 2), payload[15:]
        subpackets = []
        while total_bits:
            packet, new_payload = _decode_packet(payload)
            subpackets.append(packet)
            total_bits -= len(payload) - len(new_payload)
            payload = new_payload
    elif length_type_id == LT_NUM_PACKETS:
        num_packets, payload = int(payload[:11], 2), payload[11:]
        subpackets = [None] * num_packets
        for i in range(num_packets):
            packet, payload = _decode_packet(payload)
            subpackets[i] = packet
    else:
        raise ValueError(length_type_id)

    return Packet(version, type_id, None, subpackets), payload


def decode_packet(bits):
    p, _ = _decode_packet(bits)
    return p


def hex_to_bits(hex_str: str):
    return hex_str.translate({
        ord("0"): "0000",
        ord("1"): "0001",
        ord("2"): "0010",
        ord("3"): "0011",
        ord("4"): "0100",
        ord("5"): "0101",
        ord("6"): "0110",
        ord("7"): "0111",
        ord("8"): "1000",
        ord("9"): "1001",
        ord("A"): "1010",
        ord("B"): "1011",
        ord("C"): "1100",
        ord("D"): "1101",
        ord("E"): "1110",
        ord("F"): "1111",
    })


def version_sum(packet: Packet):
    v = packet.version
    if packet.subpackets:
        v += sum(map(version_sum, packet.subpackets))
    return v


print(version_sum(decode_packet(hex_to_bits(data))))


def eval_packet(packet: Packet):
    if packet.type == T_LITERAL:
        return packet.value

    args = list(map(eval_packet, packet.subpackets))
    if packet.type == T_SUM:
        return sum(args)
    elif packet.type == T_PRODUCT:
        return reduce(mul, args)
    elif packet.type == T_MIN:
        return min(args)
    elif packet.type == T_MAX:
        return max(args)
    elif packet.type == T_GT:
        return int(args[0] > args[1])
    elif packet.type == T_LT:
        return int(args[0] < args[1])
    elif packet.type == T_EQ:
        return int(args[0] == args[1])
    else:
        raise ValueError(packet.type)


print(eval_packet(decode_packet(hex_to_bits(data))))
