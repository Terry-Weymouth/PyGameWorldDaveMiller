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
