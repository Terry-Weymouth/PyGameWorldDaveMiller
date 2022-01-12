import math
from random import randint
from settings import NUMBER_OF_GENES_IN_GENOME, GeneCellType
from parts.Gene import Gene


class Genome:

    def __init__(self, genes=None, mutant=False):
        self.genes = genes
        self.mutant = mutant
        if not genes:
            self.genes = []
            while len(self.genes) < NUMBER_OF_GENES_IN_GENOME:
                gene_bytes = Gene.make_random_gene_bytes()
                self.genes.append(Gene(gene_bytes))

    def get_genes(self):
        return self.genes

    def create_mutant_genome_single_bit(self):
        index = randint(0, len(self.genes) - 1)
        new_genes = []
        for i in range(len(self.genes)):
            new_gene = Gene(self.genes[i].gene_bytes)
            if i == index:
                new_gene = new_gene.create_mutant_gene_single_bit()
            new_genes.append(new_gene)
        return Genome(new_genes, mutant=True)

    def create_crossover(self, mate):
        cross_point = randint(1, len(self.genes) - 2)
        new_genes = []
        for i in range(len(self.genes)):
            if i < cross_point:
                new_genes.append(self.genes[i])
            else:
                new_genes.append(mate.genes[i])
        return Genome(new_genes)

    def get_color(self, candidates):
        number_of_genes = len(self.get_genes())
        value_list = []
        for gene in self.get_genes():
            p = gene.parse()
            entry = []
            for i in range(2):
                index = self.normalize_index(p[i], candidates)
                entry.append([p[i][0].value, index])
            entry.append(int(p[2] / 256))
            value_list.append(entry)

        sums = [0, 0, 0, 0, 0]
        strength_scale = 1.0 / (0.9 * number_of_genes)
        # strength_scale = 1.0 / NUMBER_OF_GENES_IN_GENOME

        for entry in value_list:
            sums[0] += entry[0][0]
            sums[1] += entry[0][1]
            sums[2] += entry[1][0] - 1
            sums[3] += entry[1][1]
            sums[4] += entry[2] * strength_scale  # boosted average

        for i in range(4):
            sums[i] = sums[i] / number_of_genes
        max1 = max(len(candidates.get_sensors()), len(candidates.get_neurons()))
        max2 = max(len(candidates.get_actuators()), len(candidates.get_neurons()))
        new_sums = [sums[0] + 1, (sums[1] * 63.0) / max1, sums[2] + 1, (sums[3] * 63.0) / max2, sums[4]]
        new_sums = [int(math.ceil(x)) for x in new_sums]

        colors = [0, 0, 0]
        colors[0] = (new_sums[1] << 2) + new_sums[0]
        colors[1] = (new_sums[3] << 2) + new_sums[2]
        colors[2] = new_sums[4]
        colors = self.saturate_list(colors)
        # for i in range(3):
        #    colors[i] = self.satruate(colors[i])
        return tuple(colors)

    @staticmethod
    def normalize_index(cell_parse, candidates):
        cell_type = cell_parse[0]
        raw_index = cell_parse[1]
        cell_array = []
        if cell_type is GeneCellType.SENSOR:
            cell_array = candidates.get_sensors()
        elif cell_type is GeneCellType.ACTUATOR:
            cell_array = candidates.get_actuators()
        elif cell_type is GeneCellType.NEURON:
            cell_array = candidates.get_neurons()
        new_index = raw_index % len(cell_array)
        return new_index

    @staticmethod
    def satruate(color):
        if color == 0:
            return color
        while color < 128:
            color = color << 1
        return color

    @staticmethod
    def saturate_list(color_list):
        scale_value = 255 - max(color_list)
        return [x + scale_value for x in color_list]