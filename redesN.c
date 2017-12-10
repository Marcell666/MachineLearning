#include <stdio.h>
#include <stdlib.h>
#include "genann.h"

#define EXEMPLOS 500
//estou usando mil exemplos de treinamento/validacao, 500 de cada um
#define ENTRADAS 60
//tem poucas palavras, acho que poderiam ser 60

void init(double *d, int tam){
	int i;
	for(i=0;i<tam;i++)
		d[i] = 0;
}

void initM(double **d, int nLinhas, int nColunas){
	int i;
	for(i=0;i<nLinhas;i++)
		init(d[i], nColunas);
}

void leDados(double *v, FILE *f){
	
	char leDados[255];
	char *c;
	int value;

	printf("abrindo arquivos\n");

	f = fopen("base/treinamento/negDest", "rt");
	while(fgets(leDados, sizeof(leDados), f)){
		//printf("line %s", leDados);
		c = leDados;
		while (*c != '\n'){
			value = strtol(c, &c, 10);
			printf(" %d", value);
			if(*c == ' ') c++;
		}
		printf("\n");
	}
}

void leMatriz(double **v, FILE *f, int linhas){
	int i;
	char leDados[255];
	char *c;
	int value;

	i=0;
	while(fgets(leDados, sizeof(leDados), f)){
		c = leDados;
		while (*c != '\n'){
			value = strtol(c, &c, 10);
			v[i][value] = 1;
			printf("mudando para um em %d, %d\n", i, value);
			if(*c == ' ') c++;
		}
		i++;
		if(i>linhas)break;
	}
}

void erroF(char *msg, FILE *f){
	if(!f){
		fprintf(stderr, "Erro: %s.\n", msg);
		exit(EXIT_FAILURE);
	}
}

int main(void)
{
	FILE *f;

	double **inputPos;
	double **inputNeg;

	int i, e;
	double pos = 1;
	double neg = 0;

	inputPos = (double**) malloc(EXEMPLOS*sizeof(double*));
	for(i=0;i<EXEMPLOS;i++)
		inputPos[i] = (double*) malloc(ENTRADAS*sizeof(double));

	inputNeg = (double**) malloc(EXEMPLOS*sizeof(double*));
	for(i=0;i<EXEMPLOS;i++)
		inputNeg[i] = (double*) malloc(ENTRADAS*sizeof(double));



	printf("inicializando\n");

	initM(inputPos, EXEMPLOS, ENTRADAS);
	initM(inputNeg, EXEMPLOS, ENTRADAS);

	printf("abrindo arquivos\n");

	f = fopen("base/treinamento/negDest", "rt");
	erroF("ao abrir arquivo de treinamento avaliacoes negativas", f);
	printf("hora de ler o segundo\n");
	leMatriz(inputNeg, f, EXEMPLOS);
	printf("lido\n");
	fclose(f);
	
	printf("abrindo o outro\n");
	
	f = fopen("base/treinamento/posDest", "rt");
	erroF("ao abrir arquivo de treinamento avaliacoes positivas", f);
	printf("hora de ler o segundo\n");
	leMatriz(inputPos, f, EXEMPLOS);
	printf("lido\n");
	fclose(f);

	printf("comecando treinamento\n");


    /* New network with 60 inputs,
     * 2 hidden layer of 30 neurons,
     * and 1 output. */
	genann *ann = genann_init(ENTRADAS, 1, 2, 1);

    /* Train on the 100 labeled data points many times. */
    for (i = 0; i < 500; ++i) {
	for(e =0;e<EXEMPLOS;e++)
		genann_train(ann, inputPos[e], &pos, 3);	
	for(e =0;e<EXEMPLOS;e++)
		genann_train(ann, inputNeg[e], &neg, 3);	
    }

	initM(inputPos, EXEMPLOS, ENTRADAS);
	initM(inputNeg, EXEMPLOS, ENTRADAS);

	f = fopen("base/validacao/negDest", "rt");
	erroF("ao abrir arquivo de validacao avaliacoes negativas", f);
	leMatriz(inputNeg, f, EXEMPLOS);
	fclose(f);
	f = fopen("base/validacao/posDest", "rt");
	erroF("ao abrir arquivo de validacao avaliacoes positivas", f);
	leMatriz(inputPos, f, EXEMPLOS);
	fclose(f);
    /* Run the network and see what it predicts. */
	for(i=0;i<EXEMPLOS;i++){
	    printf("Output for line %d of POS is %1.f.\n", i, *genann_run(ann, inputPos[i]));
	    printf("Output for line %d of NEG is %1.f.\n", i, *genann_run(ann, inputNeg[i]));
	}
	for(i=0;i<ENTRADAS;i++)
		printf("%lf, ", inputNeg[499][i]);
	printf("\n");

    genann_free(ann);
    return 0;
}
