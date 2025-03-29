# Homeworks for Marketing analysis course

### ROOT

- Kinopoisk top250 movies parsing
  
  Here I parsed [kinopoisk](https://www.kinopoisk.ru/lists/movies/top250/?page=1) website and stored data in `pandas.DataFrame`. Then I checked hypothesis using Mann-Whitney U-test and Boostrap. The comparison was made between all ratings, ratings of films of a similar genre/decade of creation/country of production.      
  __Hypothesis:__     
  __H0__ - there is no statistical difference between `rating_new` and `rating_old`  
  __Ha__ - the difference between `rating_new` and `rating_old` exists  
  
  The results of hypothesis checking can be found in jupyter notebook using the [Link](https://github.com/Turakulov/marketing-analysis/blob/master/Kinopoisk_top250_parsing/Kinopoisk_top250_parsing.ipynb)
