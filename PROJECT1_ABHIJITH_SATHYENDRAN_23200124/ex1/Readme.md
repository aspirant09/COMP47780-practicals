1. docker volume create ex1_vol
2. docker run -v ex1_vol:/data -it –name sender ubuntu:22.04 bash
3. cd data, apt-get update && apt-get install vim, vim test.txt
4. exit
5. docker run -v ex1_vol:/data -it –name receiver ubuntu:22.04 bash
6. cd data && ls && cat test.txt
7. exit