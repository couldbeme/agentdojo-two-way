## SE table: Suites as fixed strata (headline)

Ratios are SE / naive SE. n = cells.

| pipeline | metric | n | mean | naive SE | user | inj | two-way | two-way SE | pigeonhole |
|---|---|---|---|---|---|---|---|---|---|
| Meta-SecAlign-70B | utility | 949 | 0.780 | 0.0135 | 2.72x | 0.48x | 2.58x | 0.0348 | 2.77x |
| Meta-SecAlign-70B | attack_success | 949 | 0.022 | 0.0048 | 2.35x | 0.52x | 2.21x | 0.0105 | 2.46x |
| Meta-SecAlign-70B-repeat_user_prompt | utility | 949 | 0.801 | 0.0130 | 2.72x | 0.33x | 2.56x | 0.0332 | 2.74x |
| Meta-SecAlign-70B-repeat_user_prompt | attack_success | 949 | 0.021 | 0.0047 | 2.31x | 0.62x | 2.18x | 0.0102 | 2.42x |
| claude-3-5-sonnet-20240620 | utility | 629 | 0.512 | 0.0199 | 1.95x | 2.27x | 2.82x | 0.0563 | 3.03x |
| claude-3-5-sonnet-20240620 | attack_success | 629 | 0.339 | 0.0189 | 1.03x | 3.22x | 3.25x | 0.0614 | 3.34x |
| claude-3-5-sonnet-20241022 | utility | 629 | 0.725 | 0.0178 | 2.36x | 0.33x | 2.18x | 0.0388 | 2.36x |
| claude-3-5-sonnet-20241022 | attack_success | 629 | 0.011 | 0.0042 | 1.06x | 1.27x | 1.33x | 0.0055 | 1.78x |
| claude-3-7-sonnet-20250219 | utility | 949 | 0.821 | 0.0125 | 2.59x | 0.69x | 2.49x | 0.0311 | 2.65x |
| claude-3-7-sonnet-20250219 | attack_success | 949 | 0.050 | 0.0070 | 1.23x | 2.02x | 2.17x | 0.0153 | 2.46x |
| claude-3-haiku-20240307 | utility | 629 | 0.334 | 0.0188 | 2.28x | 0.47x | 2.10x | 0.0396 | 2.36x |
| claude-3-haiku-20240307 | attack_success | 629 | 0.091 | 0.0115 | 1.25x | 1.69x | 1.88x | 0.0215 | 2.19x |
| claude-3-opus-20240229 | utility | 629 | 0.525 | 0.0199 | 2.15x | 0.65x | 2.01x | 0.0400 | 2.30x |
| claude-3-opus-20240229 | attack_success | 629 | 0.113 | 0.0126 | 1.06x | 1.87x | 1.94x | 0.0245 | 2.21x |
| claude-3-sonnet-20240229 | utility | 629 | 0.332 | 0.0188 | 1.99x | 1.15x | 2.07x | 0.0389 | 2.33x |
| claude-3-sonnet-20240229 | attack_success | 629 | 0.267 | 0.0177 | 1.44x | 1.92x | 2.20x | 0.0389 | 2.43x |
| command-r | utility | 629 | 0.308 | 0.0184 | 2.17x | 0.62x | 2.03x | 0.0373 | 2.29x |
| command-r | attack_success | 629 | 0.033 | 0.0072 | 1.47x | 0.87x | 1.41x | 0.0101 | 1.87x |
| command-r-plus | utility | 629 | 0.251 | 0.0173 | 2.13x | 0.51x | 1.97x | 0.0342 | 2.27x |
| command-r-plus | attack_success | 629 | 0.045 | 0.0082 | 1.99x | 0.61x | 1.83x | 0.0151 | 2.12x |
| gemini-1.5-flash-001 | utility | 629 | 0.342 | 0.0189 | 2.28x | 0.36x | 2.10x | 0.0398 | 2.35x |
| gemini-1.5-flash-001 | attack_success | 629 | 0.122 | 0.0131 | 1.31x | 1.57x | 1.81x | 0.0237 | 2.14x |
| gemini-1.5-flash-002 | utility | 629 | 0.324 | 0.0187 | 2.40x | 0.42x | 2.23x | 0.0416 | 2.43x |
| gemini-1.5-flash-002 | attack_success | 629 | 0.035 | 0.0073 | 1.01x | 2.11x | 2.13x | 0.0156 | 2.38x |
| gemini-1.5-pro-001 | utility | 629 | 0.289 | 0.0181 | 2.06x | 0.53x | 1.89x | 0.0342 | 2.20x |
| gemini-1.5-pro-001 | attack_success | 629 | 0.286 | 0.0180 | 1.38x | 1.39x | 1.75x | 0.0315 | 2.06x |
| gemini-1.5-pro-002 | utility | 629 | 0.471 | 0.0199 | 2.21x | 0.62x | 2.08x | 0.0415 | 2.33x |
| gemini-1.5-pro-002 | attack_success | 629 | 0.170 | 0.0150 | 1.39x | 1.14x | 1.55x | 0.0233 | 1.89x |
| gemini-2.0-flash-001 | utility | 949 | 0.393 | 0.0159 | 3.00x | 0.53x | 2.89x | 0.0459 | 3.10x |
| gemini-2.0-flash-001 | attack_success | 949 | 0.141 | 0.0113 | 1.60x | 0.92x | 1.65x | 0.0187 | 1.92x |
| gemini-2.0-flash-exp | utility | 629 | 0.399 | 0.0195 | 2.32x | 0.51x | 2.16x | 0.0422 | 2.38x |
| gemini-2.0-flash-exp | attack_success | 629 | 0.170 | 0.0150 | 1.59x | 1.07x | 1.68x | 0.0252 | 2.06x |
| gpt-3.5-turbo-0125 | utility | 629 | 0.347 | 0.0190 | 2.31x | 0.57x | 2.17x | 0.0411 | 2.44x |
| gpt-3.5-turbo-0125 | attack_success | 629 | 0.103 | 0.0121 | 1.49x | 1.78x | 2.12x | 0.0257 | 2.37x |
| gpt-4-0125-preview | utility | 629 | 0.407 | 0.0196 | 1.63x | 1.72x | 2.19x | 0.0430 | 2.41x |
| gpt-4-0125-preview | attack_success | 629 | 0.563 | 0.0198 | 0.78x | 3.48x | 3.45x | 0.0683 | 3.55x |
| gpt-4-turbo-2024-04-09 | utility | 629 | 0.541 | 0.0199 | 2.05x | 1.02x | 2.06x | 0.0411 | 2.33x |
| gpt-4-turbo-2024-04-09 | attack_success | 629 | 0.286 | 0.0180 | 1.20x | 1.79x | 1.99x | 0.0359 | 2.21x |
| gpt-4o-2024-05-13 | utility | 629 | 0.501 | 0.0200 | 1.80x | 1.43x | 2.11x | 0.0420 | 2.34x |
| gpt-4o-2024-05-13 | attack_success | 629 | 0.477 | 0.0199 | 1.28x | 2.17x | 2.37x | 0.0473 | 2.54x |
| gpt-4o-2024-05-13-repeat_user_prompt | utility | 629 | 0.672 | 0.0187 | 2.10x | 1.18x | 2.19x | 0.0411 | 2.45x |
| gpt-4o-2024-05-13-repeat_user_prompt | attack_success | 629 | 0.278 | 0.0179 | 1.16x | 2.19x | 2.31x | 0.0414 | 2.54x |
| gpt-4o-2024-05-13-spotlighting_with_delimiting | utility | 629 | 0.556 | 0.0198 | 1.74x | 1.68x | 2.24x | 0.0445 | 2.48x |
| gpt-4o-2024-05-13-spotlighting_with_delimiting | attack_success | 629 | 0.417 | 0.0197 | 1.06x | 2.60x | 2.67x | 0.0525 | 2.83x |
| gpt-4o-2024-05-13-tool_filter | utility | 629 | 0.563 | 0.0198 | 2.06x | 0.60x | 1.90x | 0.0377 | 2.24x |
| gpt-4o-2024-05-13-tool_filter | attack_success | 629 | 0.068 | 0.0101 | 1.14x | 1.77x | 1.85x | 0.0186 | 2.22x |
| gpt-4o-2024-05-13-transformers_pi_detector | utility | 629 | 0.211 | 0.0163 | 2.27x | 0.93x | 2.25x | 0.0366 | 2.49x |
| gpt-4o-2024-05-13-transformers_pi_detector | attack_success | 629 | 0.079 | 0.0108 | 1.23x | 2.86x | 2.96x | 0.0320 | 3.14x |
| gpt-4o-mini-2024-07-18 | utility | 629 | 0.499 | 0.0200 | 2.19x | 0.78x | 2.11x | 0.0421 | 2.34x |
| gpt-4o-mini-2024-07-18 | attack_success | 629 | 0.272 | 0.0178 | 1.72x | 1.60x | 2.15x | 0.0382 | 2.41x |
| meta-llama_Llama-3-70b-chat-hf | utility | 629 | 0.183 | 0.0154 | 2.16x | 0.93x | 2.14x | 0.0331 | 2.39x |
| meta-llama_Llama-3-70b-chat-hf | attack_success | 629 | 0.256 | 0.0174 | 1.43x | 2.26x | 2.50x | 0.0435 | 2.73x |
| meta-llama_Llama-3.3-70B-Instruct | utility | 949 | 0.414 | 0.0160 | 2.81x | 0.72x | 2.73x | 0.0437 | 2.92x |
| meta-llama_Llama-3.3-70B-Instruct | attack_success | 949 | 0.231 | 0.0137 | 1.55x | 1.49x | 1.97x | 0.0269 | 2.23x |
| meta-llama_Llama-3.3-70B-Instruct-repeat_user_prompt | utility | 797 | 0.395 | 0.0173 | 2.88x | 0.92x | 2.86x | 0.0495 | 3.01x |
| meta-llama_Llama-3.3-70B-Instruct-repeat_user_prompt | attack_success | 797 | 0.090 | 0.0102 | 1.75x | 1.54x | 2.13x | 0.0216 | 2.37x |

| metric | two-way ratio min | median | max | pigeonhole/two-way min | pigeonhole/two-way max | rule picks smaller one-way | two-way < larger one-way | CGM fallback used |
|---|---|---|---|---|---|---|---|---|
| attack_success | 1.33 | 2.12 | 3.45 | 1.03 | 1.35 | 10 | 5 | 0 |
| utility | 1.89 | 2.16 | 2.89 | 1.05 | 1.18 | 2 | 21 | 0 |

One-key rule understates (picks the smaller one-way SE):

- utility: claude-3-5-sonnet-20240620, gpt-4-0125-preview
- attack_success: Meta-SecAlign-70B, Meta-SecAlign-70B-repeat_user_prompt, command-r, command-r-plus, gemini-1.5-pro-002, gemini-2.0-flash-001, gemini-2.0-flash-exp, gpt-4o-mini-2024-07-18, meta-llama_Llama-3.3-70B-Instruct, meta-llama_Llama-3.3-70B-Instruct-repeat_user_prompt

## SE table: Pooled (grand-mean centring, as in #2605)

Ratios are SE / naive SE. n = cells.

| pipeline | metric | n | mean | naive SE | user | inj | two-way | two-way SE | pigeonhole |
|---|---|---|---|---|---|---|---|---|---|
| Meta-SecAlign-70B | utility | 949 | 0.780 | 0.0135 | 2.77x | 1.02x | 2.78x | 0.0375 | 3.03x |
| Meta-SecAlign-70B | attack_success | 949 | 0.022 | 0.0048 | 2.48x | 1.33x | 2.63x | 0.0126 | 2.94x |
| Meta-SecAlign-70B-repeat_user_prompt | utility | 949 | 0.801 | 0.0130 | 2.81x | 1.31x | 2.94x | 0.0381 | 3.18x |
| Meta-SecAlign-70B-repeat_user_prompt | attack_success | 949 | 0.021 | 0.0047 | 2.43x | 1.34x | 2.59x | 0.0121 | 2.90x |
| claude-3-5-sonnet-20240620 | utility | 629 | 0.512 | 0.0199 | 1.99x | 2.38x | 2.93x | 0.0585 | 3.17x |
| claude-3-5-sonnet-20240620 | attack_success | 629 | 0.339 | 0.0189 | 1.46x | 3.67x | 3.82x | 0.0722 | 3.97x |
| claude-3-5-sonnet-20241022 | utility | 629 | 0.725 | 0.0178 | 2.45x | 1.59x | 2.74x | 0.0489 | 3.05x |
| claude-3-5-sonnet-20241022 | attack_success | 629 | 0.011 | 0.0042 | 1.11x | 1.46x | 1.53x | 0.0064 | 2.07x |
| claude-3-7-sonnet-20250219 | utility | 949 | 0.821 | 0.0125 | 2.68x | 1.37x | 2.84x | 0.0354 | 3.10x |
| claude-3-7-sonnet-20250219 | attack_success | 949 | 0.050 | 0.0070 | 1.44x | 2.51x | 2.71x | 0.0191 | 3.08x |
| claude-3-haiku-20240307 | utility | 629 | 0.334 | 0.0188 | 2.29x | 0.60x | 2.15x | 0.0404 | 2.52x |
| claude-3-haiku-20240307 | attack_success | 629 | 0.091 | 0.0115 | 1.46x | 2.30x | 2.53x | 0.0290 | 2.87x |
| claude-3-opus-20240229 | utility | 629 | 0.525 | 0.0199 | 2.15x | 0.69x | 2.03x | 0.0404 | 2.43x |
| claude-3-opus-20240229 | attack_success | 629 | 0.113 | 0.0126 | 1.40x | 2.67x | 2.84x | 0.0359 | 3.15x |
| claude-3-sonnet-20240229 | utility | 629 | 0.332 | 0.0188 | 1.99x | 1.17x | 2.08x | 0.0391 | 2.47x |
| claude-3-sonnet-20240229 | attack_success | 629 | 0.267 | 0.0177 | 1.63x | 2.59x | 2.89x | 0.0510 | 3.16x |
| command-r | utility | 629 | 0.308 | 0.0184 | 2.21x | 0.97x | 2.19x | 0.0404 | 2.58x |
| command-r | attack_success | 629 | 0.033 | 0.0072 | 1.62x | 1.40x | 1.89x | 0.0135 | 2.31x |
| command-r-plus | utility | 629 | 0.251 | 0.0173 | 2.25x | 1.50x | 2.52x | 0.0436 | 2.80x |
| command-r-plus | attack_success | 629 | 0.045 | 0.0082 | 2.03x | 1.12x | 2.10x | 0.0172 | 2.38x |
| gemini-1.5-flash-001 | utility | 629 | 0.342 | 0.0189 | 2.40x | 1.32x | 2.55x | 0.0483 | 2.88x |
| gemini-1.5-flash-001 | attack_success | 629 | 0.122 | 0.0131 | 1.50x | 2.29x | 2.55x | 0.0334 | 2.91x |
| gemini-1.5-flash-002 | utility | 629 | 0.324 | 0.0187 | 2.43x | 0.86x | 2.38x | 0.0444 | 2.72x |
| gemini-1.5-flash-002 | attack_success | 629 | 0.035 | 0.0073 | 1.14x | 2.41x | 2.48x | 0.0182 | 2.81x |
| gemini-1.5-pro-001 | utility | 629 | 0.289 | 0.0181 | 2.15x | 1.23x | 2.26x | 0.0410 | 2.63x |
| gemini-1.5-pro-001 | attack_success | 629 | 0.286 | 0.0180 | 1.74x | 2.74x | 3.08x | 0.0556 | 3.33x |
| gemini-1.5-pro-002 | utility | 629 | 0.471 | 0.0199 | 2.27x | 1.15x | 2.34x | 0.0467 | 2.67x |
| gemini-1.5-pro-002 | attack_success | 629 | 0.170 | 0.0150 | 1.72x | 2.54x | 2.90x | 0.0435 | 3.19x |
| gemini-2.0-flash-001 | utility | 949 | 0.393 | 0.0159 | 3.07x | 1.21x | 3.15x | 0.0499 | 3.35x |
| gemini-2.0-flash-001 | attack_success | 949 | 0.141 | 0.0113 | 2.21x | 3.05x | 3.63x | 0.0411 | 3.90x |
| gemini-2.0-flash-exp | utility | 629 | 0.399 | 0.0195 | 2.37x | 1.15x | 2.43x | 0.0475 | 2.83x |
| gemini-2.0-flash-exp | attack_success | 629 | 0.170 | 0.0150 | 1.80x | 2.24x | 2.69x | 0.0404 | 2.97x |
| gpt-3.5-turbo-0125 | utility | 629 | 0.347 | 0.0190 | 2.37x | 1.17x | 2.45x | 0.0464 | 2.72x |
| gpt-3.5-turbo-0125 | attack_success | 629 | 0.103 | 0.0121 | 1.72x | 2.23x | 2.63x | 0.0320 | 2.98x |
| gpt-4-0125-preview | utility | 629 | 0.407 | 0.0196 | 2.00x | 2.80x | 3.29x | 0.0646 | 3.55x |
| gpt-4-0125-preview | attack_success | 629 | 0.563 | 0.0198 | 1.30x | 4.23x | 4.31x | 0.0853 | 4.48x |
| gpt-4-turbo-2024-04-09 | utility | 629 | 0.541 | 0.0199 | 2.08x | 1.27x | 2.22x | 0.0442 | 2.61x |
| gpt-4-turbo-2024-04-09 | attack_success | 629 | 0.286 | 0.0180 | 1.80x | 3.27x | 3.59x | 0.0648 | 3.87x |
| gpt-4o-2024-05-13 | utility | 629 | 0.501 | 0.0200 | 2.09x | 2.74x | 3.30x | 0.0658 | 3.54x |
| gpt-4o-2024-05-13 | attack_success | 629 | 0.477 | 0.0199 | 1.84x | 3.28x | 3.62x | 0.0722 | 3.86x |
| gpt-4o-2024-05-13-repeat_user_prompt | utility | 629 | 0.672 | 0.0187 | 2.14x | 1.40x | 2.35x | 0.0441 | 2.71x |
| gpt-4o-2024-05-13-repeat_user_prompt | attack_success | 629 | 0.278 | 0.0179 | 1.64x | 3.11x | 3.37x | 0.0603 | 3.64x |
| gpt-4o-2024-05-13-spotlighting_with_delimiting | utility | 629 | 0.556 | 0.0198 | 2.05x | 2.86x | 3.37x | 0.0669 | 3.61x |
| gpt-4o-2024-05-13-spotlighting_with_delimiting | attack_success | 629 | 0.417 | 0.0197 | 1.72x | 3.55x | 3.82x | 0.0751 | 4.02x |
| gpt-4o-2024-05-13-tool_filter | utility | 629 | 0.563 | 0.0198 | 2.10x | 0.98x | 2.09x | 0.0414 | 2.49x |
| gpt-4o-2024-05-13-tool_filter | attack_success | 629 | 0.068 | 0.0101 | 1.18x | 1.85x | 1.95x | 0.0197 | 2.40x |
| gpt-4o-2024-05-13-transformers_pi_detector | utility | 629 | 0.211 | 0.0163 | 2.31x | 1.22x | 2.41x | 0.0393 | 2.78x |
| gpt-4o-2024-05-13-transformers_pi_detector | attack_success | 629 | 0.079 | 0.0108 | 1.41x | 3.17x | 3.32x | 0.0359 | 3.48x |
| gpt-4o-mini-2024-07-18 | utility | 629 | 0.499 | 0.0200 | 2.24x | 1.17x | 2.32x | 0.0463 | 2.67x |
| gpt-4o-mini-2024-07-18 | attack_success | 629 | 0.272 | 0.0178 | 1.90x | 2.33x | 2.84x | 0.0504 | 3.13x |
| meta-llama_Llama-3-70b-chat-hf | utility | 629 | 0.183 | 0.0154 | 2.29x | 1.53x | 2.56x | 0.0395 | 2.83x |
| meta-llama_Llama-3-70b-chat-hf | attack_success | 629 | 0.256 | 0.0174 | 1.56x | 2.55x | 2.82x | 0.0491 | 3.07x |
| meta-llama_Llama-3.3-70B-Instruct | utility | 949 | 0.414 | 0.0160 | 2.89x | 1.37x | 3.04x | 0.0486 | 3.30x |
| meta-llama_Llama-3.3-70B-Instruct | attack_success | 949 | 0.231 | 0.0137 | 2.17x | 2.97x | 3.54x | 0.0485 | 3.86x |
| meta-llama_Llama-3.3-70B-Instruct-repeat_user_prompt | utility | 797 | 0.395 | 0.0173 | 2.92x | 1.12x | 2.96x | 0.0513 | 3.20x |
| meta-llama_Llama-3.3-70B-Instruct-repeat_user_prompt | attack_success | 797 | 0.090 | 0.0102 | 1.97x | 2.05x | 2.67x | 0.0271 | 2.98x |

| metric | two-way ratio min | median | max | pigeonhole/two-way min | pigeonhole/two-way max | rule picks smaller one-way | two-way < larger one-way | CGM fallback used |
|---|---|---|---|---|---|---|---|---|
| attack_success | 1.53 | 2.83 | 4.31 | 1.04 | 1.35 | 4 | 0 | 0 |
| utility | 2.03 | 2.48 | 3.37 | 1.06 | 1.2 | 4 | 5 | 0 |

One-key rule understates (picks the smaller one-way SE):

- utility: claude-3-5-sonnet-20240620, gpt-4-0125-preview, gpt-4o-2024-05-13, gpt-4o-2024-05-13-spotlighting_with_delimiting
- attack_success: Meta-SecAlign-70B, Meta-SecAlign-70B-repeat_user_prompt, command-r, command-r-plus

## Coverage (R=2000, B=500, 28 pipelines per metric)

| method | mean attack_success | mean utility | min attack_success | min utility | max attack_success | max utility | median SE/true SD attack_success | median SE/true SD utility |
|---|---|---|---|---|---|---|---|---|
| naive | 0.659 | 0.613 | 0.4 | 0.486 | 0.908 | 0.694 | 0.479 | 0.455 |
| user | 0.759 | 0.929 | 0.356 | 0.86 | 0.914 | 0.948 | 0.636 | 0.96 |
| inj | 0.848 | 0.519 | 0.708 | 0.3 | 0.926 | 0.788 | 0.792 | 0.323 |
| twoway | 0.913 | 0.935 | 0.876 | 0.924 | 0.935 | 0.946 | 0.903 | 0.918 |
| pigeon | 0.949 | 0.952 | 0.915 | 0.938 | 0.978 | 0.962 | 1.05 | 1.036 |
| twoway_pooled | 0.967 | 0.966 | 0.918 | 0.946 | 1.0 | 0.995 | 1.259 | 1.055 |
