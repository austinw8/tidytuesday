#2024, Week 23, Cheese

library(tidyverse)

cheeses <- readr::read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2024/2024-06-04/cheeses.csv')

head(cheeses)
distinct(cheeses)

