from random import randint
from settings import NUMBER_OF_GENES_IN_GENOME
from parts.Gene import Gene


class Genome:

    def __init__(self, genes=None):
        self.genes = genes
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
        return Genome(new_genes)
