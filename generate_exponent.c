
#include <gmp.h>
#include <stdio.h>
#include <assert.h>

int main(){

  mpz_t exponent_m, addend;
  unsigned long seed;
  printf ("%d\n", seed);
  gmp_randstate_t rstate;
  gmp_randinit_mt(rstate);
  gmp_randseed_ui(rstate, seed);
  printf ("%d\n", seed);

  //create random number between 2^60
  mpz_inits(exponent_m, addend);
  mpz_ui_pow_ui(addend, 2, 60);

  mpz_rrandomb(exponent_m, rstate, 60);
  //add 2^60
  mpz_add(exponent_m, exponent_m, addend);
  gmp_printf ("%z", exponent_m);
  mpz_clears(exponent_m, addend);
}
