---
title: 푸리에 급수 (1)
date: 2026-10-25
---

## 렌더링 확인

인라인: 오일러 공식 $e^{i\theta} = \cos\theta + i\sin\theta$에 $\theta = \pi$를 넣으면 $e^{i\pi} + 1 = 0$이다.

$$
f(x) \sim \frac{a_0}{2} + \sum_{n=1}^{\infty} \left( a_n \cos nx + b_n \sin nx \right)
$$

$$
\begin{aligned}
a_n &= \frac{1}{\pi} \int_{-\pi}^{\pi} f(x) \cos nx \, dx \\
b_n &= \frac{1}{\pi} \int_{-\pi}^{\pi} f(x) \sin nx \, dx
\end{aligned}
$$

한글 텍스트: $\hat{f}(n) = 0 \quad \text{(모든 } n \text{에 대해)}$

$$
\sum_{n=-N}^{N} \hat{f}(n) e^{inx} = \frac{1}{2\pi} \int_{-\pi}^{\pi} f(y) \sum_{n=-N}^{N} e^{in(x-y)} \, dy = \frac{1}{2\pi} \int_{-\pi}^{\pi} f(y) D_N(x-y) \, dy
$$

달러 기호: 가격은 \$5다.
