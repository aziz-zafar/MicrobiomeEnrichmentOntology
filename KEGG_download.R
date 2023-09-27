
if (!requireNamespace("BiocManager", quietly = TRUE))
  install.packages("BiocManager")

BiocManager::install("KEGGREST")

library(KEGGREST)
library(stringr)
library(tidyverse)
human_pathways =keggList("pathway", "hsa")
head(human_pathways)


pathway_data <- data.frame(Name = human_pathways)

# Split the "Name" column into two columns: Label and Pathway Name
pathway_data <- pathway_data %>%
  separate(Name, into = c("Label", "Pathway Name"), sep = " - ")

pathway_data$ObjectID <- rownames(pathway_data)

# Export the data to a CSV file
write.csv(pathway_data, "human_pathways.csv", row.names = FALSE)
