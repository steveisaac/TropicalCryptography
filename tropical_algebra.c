
#include <gmp.h>
#include <stdio.h>
#include <assert.h>

int main(){

  mpz_t M[30][30];
  unsigned long seed;
  printf ("%d\n", seed);
  gmp_randstate_t rstate;
  gmp_randinit_mt(rstate);
  gmp_randseed_ui(rstate, seed);
  printf ("%d\n", seed);

  element_range = 2001
  for (int i = 0; i < 30; i++) {
    for (int j = 0; j < 30; j++) {
      mpz_init2(M[i][j], 64);
      mpz_urandomm(M[i][j], rstate, 2001);
      mpz_sub_ui(M[i][j], M[i][j], 1000);
    }
  }

  for (int i = 0; i < 30; i++) {
    gmp_printf ("%d %z\n", i, M[0][i]);
  }




  for (int i = 0; i < 30; i++) {
    for (int j = 0; j < 30; j++) {
      mpz_clear(M[i][j]);
    }
  }
}
