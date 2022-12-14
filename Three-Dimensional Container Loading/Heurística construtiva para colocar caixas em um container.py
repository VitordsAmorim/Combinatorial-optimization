from py3dbp import Packer, Bin, Item


def define_listas(list_container, limit_container):
    """Dictionary structure (name, width, height, depth, weight, item quantity)"""
    weight_of_boxes = 1
    list_of_items = {
        'caixa_1': ['cx1', 229, 483, 610, weight_of_boxes, list_container[0]],
        'caixa_2': ['cx2', 165, 330, 457, weight_of_boxes, list_container[1]],
        'caixa_3': ['cx3', 229, 406, 660, weight_of_boxes, list_container[2]],
        'caixa_4': ['cx4', 216, 457, 533, weight_of_boxes, list_container[3]],
        'caixa_5': ['cx5', 203, 229, 381, weight_of_boxes, list_container[4]],
        'caixa_6': ['cx6', 178, 356, 533, weight_of_boxes, list_container[5]],
        'caixa_7': ['cx7', 152, 114, 325, weight_of_boxes, list_container[6]]}
    if limit_container == 36:
        list_of_boxes = {'container_36': ['container_36', 800, 700, 1000, limit_container * weight_of_boxes, 1]}
    else:
        list_of_boxes = {'container_70': ['container_70', 1100, 900, 1400, limit_container * weight_of_boxes, 1]}
    return list_of_items, list_of_boxes


def packing_of_boxes():

    packer = Packer()
    list_36, list_70 = [4, 4, 2, 2, 2, 2, 20], [7, 7, 5, 5, 5, 6, 35]
    max_number_box = [list_36, list_70]
    lim_box = [36, 70]

    box_list, container_list = define_listas(max_number_box[0], lim_box[0])

    """Container registration"""
    for item in container_list:
        for quant_caixas in range(container_list[item][-1]):
            packer.add_bin(
                Bin(name=container_list[item][0], width=container_list[item][1], height=container_list[item][2],
                    depth=container_list[item][3], max_weight=container_list[item][4]))

    """Boxes registration"""
    for item in box_list:
        for i in range(box_list[item][-1]):
            packer.add_item(
                Item(name=box_list[item][0], width=box_list[item][1], height=box_list[item][2],
                     depth=box_list[item][3], weight=box_list[item][4]))

    packer.pack(bigger_first=False, distribute_items=False, number_of_decimals=3)

    for b in packer.bins:
        print("\n    ", b.string())

        """print("Fitted boxs:")
        for item in b.items:
            print("    ", item.string())"""

        print("Unfitted boxs:")
        for item in b.unfitted_items:
            print("    ", item.string())
        print("*************************")


if __name__ == '__main__':
    packing_of_boxes()
