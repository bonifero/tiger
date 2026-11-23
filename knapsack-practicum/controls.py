"""Rounded ttk controls; native keyboard behavior and no runtime image dependency."""
import tkinter as tk
from tkinter import ttk

# Antialiased PNGs are embedded so PyInstaller needs no external theme files.
CONTROL_FONT_SIZE = 10
_ASSETS = {'card': 'iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAACfUlEQVR4nO2ZT2sTURTF732ZpElGKIgbBZFsK7pwU/Ih3LjpQqEgfqmCGxcuzEIQFy5dhoALQSyI1FBLU2pjklYnmcy8mSvndaaOaVIoE5sJzIFHJgzvnl/OzJs/N0xTJCKKmcP4e6cndwLt3PV8v26xKuowICI1beoFCslSBdIS+qVisVmw7M+3rvPuLM9Y1hS4AjMHW1sfig8frW0Iy2NLjetVu7x6rWoTXxJrUkJEv4cBef74eL/rNFn45dvX26+Y2Y+9aZbeixjgr/v9B4d9t4UZCYUiouc0wrgoPOAFzyTD+V8W7dj53n3685d3kpj/T8E5KoxqmxzgCe8kSxKugM8vu71NZxzGNJh8VdLwhDcYkkzUaDTMxs5e7/7RYOiISBCNq1aAAQawxGxmKbbb7bJlFV7cWK1Uo/P4skt0HoKngAEsYDrb8+1gsOGfHteJdbEQ+WABk6E21x+hZxab5NJeReYhBguYwKa22we3V0pWXU7hFnFoJ6XAAiawqXKpfM+urNhM2UmQiQRMYFPEvG5XzEI+d5tZoELDxLyuSLjEYM6Y2OTIJbO0KbuSLCyKC5UDplWeYFrlCaZVnmBa5QmmVZ7gPBLM3rPWX7EiFk8ke09cAiYWT5FIyxkFWTsflWESaSnXcz85o7ETvTRlIUoBC5jAptZqN/fGnm5GL01ZeC8JwQImsJmenDA915KdBLUQgwlsCv0PdvtvOocnH6N+4ez+3P9XAAawgOmsN1Or1Vytg83u8WgYXXYWcahDeIMBLGBajvbbUjQwl6IFHCuOFk30ztHwyX7Xefdj4A4GjjaVg5RDiwhqoSZqwwNeSe+kpt6Hs/Q3xB86E4nXEeykHgAAAABJRU5ErkJggg==',
 'card_tint': 'iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAADMklEQVR4nO2ZTU8TURSGz7kz7XSY0iISDJGkadCNRBfGSFj6C1wZTFxg1IS486e40pAYIgsTwRW/wCXBGENicINKCIJasdDC0E5n7j3mXDoELH7UKW1N+i6afs779Nxzb3PeIhwjIhKIqMLH+T3KlEvusF/xRxFFjJQEAHHcR38jBSgMIFJ+LB6bT9jOUm8Xrv7KM5R5DJyBiHJy8nXs+o0LY6ToVsXzRuOxRLo76QBinVw/iQjA8yRUPK/wedOdR4HP5l68m0FEP/Q+/P4jdi+JzGuIwfL61uV00n7cnbSukuILAkgJhAg13/BfRATCMAAtCwAFwM6u96qwW7p//uypNyFDDSARmYgYfPi0eSedSj20E7HuUgkCRP0eXs+ItasR8boTAdk2mKWyv1MoFh8MDfZNhSwQmoalfb+aH+8/0/M08BGUAokIBjRBRCCFAMOMEeS+bt8+l+mdDpnE7OysvrP2JX8plU48kgEqpUA1C47FXuzJ3szALMzEbHorrqysJBQZ006X3VXttXq3aGSxJ3szA7Mwk36eb1Zz22P9p9PP3V3dczU7u5kigsBJgpn7XriZ6e+ZEXz+QAD3SOnKNXoj1C1mYBbNxGfjx42NTDyWWnJsx5EM2fjdWpcIgAwB6JZct+IXh4XAxMWEZTm691oMx2IGZmEmZhMIOGJZBjTqEG6EmEUzAY4IIIxj1N+vE5BmIoyL6onerqKmn3f1qgMYVZ0KRlWnglHVqWBUdSoYVZ0KRtVJzLuNFApAqhDnEW0mYiakiiCgBc5KOI6ANhERCM0EtCAUld+WPc/lrIQHlpbDARCzMBOziezAwJr0g3nL0kNTy+cSBJ5HgJiJ2fYzOROe6G6kNqggATGLZkJUOptR7tZcLldc5JSJg5wWwklmYBZmOshmstlsWaAcd/dKe7oXqflLTQSKvZmBWZjp/4jfYH8GlRwa8gvfNvN3Ffk7tg0GBzkAeslPojeJr80e7MWe7F2F4wBTt9pBksWJJsevQ4hTy+tbi4qaEgEbRyLgwT4dAYfpqub6mxAdDWPUNMx0NSJpSIgeyKBAUh6E6BMTV/4coh+CbJu/IX4Ar5L+g2/ErlYAAAAASUVORK5CYII=',
 'chevron': 'iVBORw0KGgoAAAANSUhEUgAAABIAAAAOCAYAAAAi2ky3AAAA/klEQVR4nGNgGBLg////jOTIYQX19fVMxIjhBcmF9ULoGuuh7KjMCkFsBiIEIE5mTKxsFeXgELiZXtqd1djY+K++vp4FhEHspKJ2QxFhqfvPv3E5grSEhq5ihmlH8S/IpmvXtBmFlR5lcHPzTvn6+UPqjO7yOSA5kCHcnNxn/v37s+Q328dMSQaGH42Njf9BTsAwCGYYyPaM0p4UHn7+2Z8+v49l+P37DDsX39V/f38vmtpelIjkCLAhOEFa2kxWEJ1e1pueUz3xf271xP9ZlX3zwN5ZtYoZGgzEAVC4gA0r7c7KrOiZAQ9wUqMfrpEBBsgwABmEhoYyI8fO0AEAhlZsK+V1fTUAAAAASUVORK5CYII=',
 'chevron_active': 'iVBORw0KGgoAAAANSUhEUgAAABIAAAAOCAYAAAAi2ky3AAABAUlEQVR4nGNgGCLgPyN5cthAfT0Tpth/TDF8QCv0kRCGxnoIW9f7kiA2A5lQnfyf0SDxmSg7D89Ng4TXWQyNjP/s6/+z2Nv/ZwGx9WKfGLJLKN43fPDGEaQjNPQ/M0w3qn/r/zOFXmNgvMv1JoOFS2TKr6+vUy8sEpsDkgIZwsrGd+b//79LGFm+ZZ6VlPrB0Mjwn4GB8T+mQTAvNDL+M0h4lcLGJTr795eXsUyMf88wsPJd/ff396Lz84USET6AGIITGKedYQXRhgmv042Tv/w3Tv763yjh3TyEd0iIOVDYgGiDhNdZRonvZiACnNToh2tkgAJyDEAGoauYkWNn6AAA7EpjvraWPMYAAAAASUVORK5CYII=',
 'chevron_disabled': 'iVBORw0KGgoAAAANSUhEUgAAABIAAAAOCAYAAAAi2ky3AAABDElEQVR4nGNgGBLg////jOTIYQX19fVMmGL/McTwgtmrdgiB6P//ERph7GnTlgpiswRZISMIr9p2SFSIl//mik2HshgZGf/t37+fBYRB7IWrdxtKq2nc1zB2dgTpWbVqFTNMPwuMwcgIMuc/E8OXF+/+cEg2CAqJTF2x6eAvR0f7OSB5kCH8AoJnfv/+tYSbges4SC3IcLh+bGHT2Nj4b8WmgynCouKzX796Ffv/998zvAJ8V3/++rko1MsqEUnvf7xhNHPmGVYQvWLT4fT1O0/937D79P81207Mg3jnPzNJMQcKF4hhh7JWbz06AxbgJEc/TCMDgo3XAHhgYwOgwITFDCMj41+SXTKgAAAApYZrGnovWwAAAABJRU5ErkJggg==',
 'field_disabled': 'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAABlklEQVR4nO2WO07DQBCGZyaJsUOCEinimQIaCiQ6OkRBwXXgAFwCqDhDfARERUuHRJEmFIBIQAGB8/BrB/3GFFAQHnbHJ620srzf7I53d8xERKrKzKzo3z48r01ZpS1VWh6PxkTETF+iajs23rryg/BssTFz+cGJDh602+2Z+8fhQf955A18o36kP2oD3yjGwgHXe5Ci67qiqk637502as7Gy8CnKPBNnK7ouyQy4el61d6LzcKmqm67rjtKZn9993i4NFfbffHGATGXkJdvmz+ClITVim3ddJ+OmvP1Pb7u9VZLBeeibFvFNF2/lb+D5OtwHERhPFoX0uJOpVK2jDGUgRwwXHDCLUyyUixIEpUygpk1cZKs4AOHGc38Mwy3TN7nf4FZKGfkP8Ak/lM0EcE9SLmhKvx2e+YRROEWJdOJYoNjndmJVlVOnGQ6QhydeN4wEEk2VBYrUbjghFuas7PtMIyOK2VLUCz+GEThgAtOuKXVahWW5mr73b53jkqU3oIoDvFPWjqG4YALTrhzL/qJPM/flldq5nvY3EaKlwAAAABJRU5ErkJggg==',
 'field_focus': 'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAB9UlEQVR4nO2Wv2sUURDHv/Pe2zPrgeCRHCkSVJAUAVMFC4mFRSohXQqx0ZC/QSstLO0EC4uAlY12ASsLC8UiWCmkCBdiuCuSSzglcNnk3o+R2c2eqW7N5a7LFwYeu/M+M294fHcJqZgAYlndfrw/HcXxXfbhevAJQCD0EoOVjkFa/bJJ8mXt7ej6aSbli5sPN65U4uoL52m5fazLgRXOIkUB5Uu+bTSvtJLm89q7qQNhExbf6+mxxfhy0vrcQWVW8x7u3ymFiaphMEC9+wfLuQloNB19/NZRnsZQQuv7YVy5t773IUmTZh/tvppZYn7wbP+4VreB+1StboMwhCVMYdPMcmNK25GfDDarL6/SZFWTc/8654LR0KmTGAPUm54XnvxmAjkfHd1SZRXNtzsjpYW5CAK3LkvUOgtTEN08A8heYQhLmMJWDLrBUHxt3DD/x8x7SfYKI2VBsbDlqlh5J9XPA88lDGGdTM8qcDbGQcBzdVkMOttl70MXBQp1MaJCKVBmN6krDkicswip6UfyLDKDKcIMCOvEJyNF4C1CoO0dR7mXnAdOBKQsBBK2agf7qVw66qx+tanVSnWxa++zcAXRzXNZ58IQljCFrX6sTGxo8m+CHlVPX/+xmw3H/dr1ZsOxMIQlTGEP/ZNJw//oZ30M7bflL/13c6lAr3gzAAAAAElFTkSuQmCC',
 'field_hover': 'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAABq0lEQVR4nO2WO0scURiG3/fs7K6XsAYvYKOogRQhgkUgKQxiYSMW/oFU5nek8B/YijZJt4VJEWxSBNEigRRCJE2MijaCF3SJl9ndOa98Mxq0yK4ss50PnOHAzPec4R3O+YYAIIkkZfPFTxvPMkHLa1ADYfkSEIhaEMrnWgBxJ6pers5MP/912xncTD4sfysIXbOPC/m3/b0d7e1t+ev62sRvBeDsPMTu/unZ++XfC8TRO5Kl2F0sFjPoGWuthKdfX448edHXCeSyzt+qvS8sV7zbOwa+r//5kc13jONg5SK+s/BxY25zP5KkUJL3PrnYiOqMm+esxmrNYS5zxqvOL60/7eks/JwaHQyCDCiBrJfLf5AAEqpG0Oe17erBcWnYeXFiqK87F2QAH38PNAyZOMxlTnM7Rzf4qC2nBjKvhcxpbiehYrEgZaQ47ooD05f/g6BDk3EPC9TjIaK6OCjVHXwXQY5E1g4opAwJmdt5+e2/52XbzWnuaJrT3M5RX7b2DsvVCHCk7MhtFClxmMuc5m5+wyk2uWUy7aZ/Ugrjpv9m8lXS9JPsmvfbcgWzrYekOAfOsgAAAABJRU5ErkJggg==',
 'field_normal': 'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAABaUlEQVR4nO2Wv0rDUBTGz7n9GxsqaBed2qWD6O7i6Jv4HA6+gbtP0FdwdBFcBItDpbSDVCqtYElJmzb55LttoYjYiMnWDy4cbu75neS7NzlREREAqqpg3OwOjop55wwi1Ynvc0rld6HoOFzUnQT+3XG18rzOzK6C+1arvO8eXhVymYtdt1gq5LlsR+JqGoh8emb80vNuhl7vUlVHZEuj0cj0+3Bbr6OHEEAYgWI4/+MImctEssgk21ZvtofXvABgCsCWiKJFEMUZi5uyaWSQRab197H9Xi87zlPtwM0u/d7k+SZxL9F58+Yj3z8xKnpe2StZx/F/uKwYZJJtjGotn7MnyJ6ihAQyyTYCmSVgy09Ssk1K8JWUBVKV2RbYpK1FsSxK8g3+LhhRyaVUBGSbCOgEMyTxFV2Xkkm2geB28DEO7GwCT6JLBplkp95wJO2Wqb83/fhaNP3JeDoLbdM/rddt07cbm+ZvyxedO/GSN5tAXwAAAABJRU5ErkJggg==',
 'field_pressed': 'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAABz0lEQVR4nO2Wv0scQRTHv292vNOLUTwvGCQBhWBxkCo/uhAUhKQwpLEKpNE/IlUKK1s7kaQRBDFNSCAKgYiky48qcIUIBhRR4p1ozJnd250n39trlJDT9a7zAzMsuzuft/OYfTOCKiqAsEPPk92879sHntU+Fx7xIW//DzW2DVEoP9Pp8PPOu1xBTzrji/vPVju2Drsnbt1MjT+8k7nSkzVwDpA6elXAGGCn5LDyvfxnbSN41dtefPllbuCAbsHogpe/NtqG/dLy85Hs3bFHilynOI6t8+Wnkd19Na+XBLPvS9/QmR0s/HpzVJ1/78j21OS8Et+vqDssqyZpfkUdHXTRSbfkHm8O5PszP95OdtlMKySKIJxyEpwDPA9a/gt9+mIvLKyXb5sg9IaH7nWkuq4C4QXkhGPpoItOuk3KoP96t8d867mz/i9qS4hOuo2DVhgVDSaMIHQzIVJvKSah5pQLZPxsXAaoy2WKzpQiZcltNFr7o42BtFivIUXiBHTSbQKH9e1iVK2sDSkYEvd00m1SNvr46etBsPc7jsqSmxTnYgdddNJtios3Vtc2gumZDzDpFlSshUYRkKRZC6WDLjrpbvqWKc3f9OPXmnZsOQY8hFiAKp/sngAAAABJRU5ErkJggg==',
 'primary_disabled': 'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAABrElEQVR4nO2Wv0ocURSHf+fcO390iaJmFcRCi1gIdhY2IhY+Qt4gdXwDC9/AVCl8gs0jpBCxSZEuYKGFIiLoiqKyOjM7c46c3QykUFfjTudXXYbhO3cOnPMbAgBVJSJSOx+dJnNh5JdEdTpNMgBMeBbRKA7BREdZmu9OT8Z7/zp9efi1fzE0OfJhg0BfwK7mGfCBRw87tCwjgAukddxMt06vbteJ6KbjbjQabnn588CdpNujo9FCs5lApJDyi16KyZgd1+sxLi/T34Mcrezs/LjvXPDg5G5zvD7w9eyslTFTAFCviz+Bqoi2JyZq4Xnz/tunqcE12ju5no05+gOoFxH6f3mJKjMrQHki6TxHCFfjOArzvMDb5QaRucxpbibCjHPQ1/b8OczVdWKGVdG2Z+g/ZG6uSF5CVqBS+L1AL95b9KIW9W2CH0FtVQQVFVFz26o4LAoba+3bRKsqdZ049Cmyn5RQ5r2zda39WNfeOyRJmpmb56aG9wuR72NjMVtY2AtvkYto21zmNHf1kamPhL7zQY3/juBrQr/I2y2FdkJ/cfZjN/TL6lX9tjwAB0EBWQhuydEAAAAASUVORK5CYII=',
 'primary_focus': 'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAB/0lEQVR4nO2WP2sUURTFz31vZpfVOGp21ayVggoGRQsrxUIwIJLCL7DYiKV+Awu/gVYiNrJNSGUhIRDFQuwsFCWCClqZqBv/DFknuzPvXTmzWQmCyY5JuhzmwR2G93vv3nlzzwgAqKqIiDJuPtLR0OCsBw50O4Dk17+lgJbKgAE+ph5PG+dldiUz6AfNKY3CMm4aiyvbKthuDYAdGFjOA78StCce6720gxsiEufsyUm1e0ZR+TSHJ7UaTi20gJfvE/8jdpovMiB8V2TlxKGKqdaAVgvP99dx7usskjz95rTe2rsP116/SbsPn8Xh/LdMNC/Y4BIBRoYDHT8TpceOhqUvn3G7cUGuy/0ZPRIKXgl8cPfBd5lrORmqCGtbSAJgMVHUa1avXtqtCpOliuNGMoxFQyi9eNfB/EIPzpR9weE8wLlkkEUm2azyQWuhP+NMVbXwzleKc8kgi0yyjQdSZmjNqqexkJZZQjbD/G49O/9bfRbZAx7E/9fWAmtqq0RryrCfM9i4zwx/WGQbA4SMnd+4T831WEo2X/IH5yA7o4DGs65MJG/bArLIJNtogJl4Ed2Th8sYqVply6XRmILDml67JoMsMsk2l8fkrctwZ7hqzPjpKK1XrbaXPNpJwbHkwblkkEUm2Ztvmbqa6RdQ3/S9Q276jYvLps+Hm/nb8hsrOkrvVJcZ1QAAAABJRU5ErkJggg==',
 'primary_hover': 'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAABfUlEQVR4nO2WvUoDQRDH/zO3ySUIivjVGghBDuwsbEQsBCu18Q2s9Q0sfAOtLHwCK7USLERsLOyEICEQWz9AFCQfd7cjc+FQBHOR3Fn5qxZ2+c3MsswsIUIIINFVebXmOY67AA6nbdAGBIReEISNC1jnPgzbV/XTSvWrk+JFeeV6mIsTuwTaJHaGQKxyJOg/z4iF2PBdIIe2+bRTP5t/Uzdh48jxsFgM/NcLkx+dC9rPetjGFfWPEIjZuOMIOi83JjeyVMVlM8qvslbdM4XJLb/50CHiXB95/4SIWD9XnMoHrcf92om3TTPr1YoV5xYEA7E0gDxGQCwQBEzhLFvLy2wKedgAKcgVUpc6IzdgS1HEX995L6hbBWyJhchPKfPvkLo58Z0PgtaBjOH/AEn8X1EirP0cWUEQJhHtnlkEEXUzwI1uF9XBk54bkZMbzGzPbdDqgE20k4YdbKBOdfPdsVcDwgPjjrEOiwGDiDrUpU51/8XIlIyHfhw9o2/LByXc3Q/AVoT/AAAAAElFTkSuQmCC',
 'primary_normal': 'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAABiklEQVR4nO2WvUoDQRDH5z93Fy4RLGJMGgttUgQUBbGzsPARUomCYK1vYOEbaJVCEBQbfQQLCzsRFIUUabSwSQwpBJOQy+7IXAhoinyYxCq/amHhNzuzH7OgEAERREfLu+WMw9F1EjtvmzWdAXUBQsJulAj8Zmzt7ukskf/pRHuwtlWYDiLJIwbvEZwpgGkQRCyRmC8r9tRrlA7vL9Of6gZlr5zMbDbqVyu3rh9fDWplEjGW0Mqob0QAOOxFE9SsVx7qsfhG/uO6Fqa/slM89mLJ/aBabBDY08z7N/9CSGzgxVKRoFo6eTxPHWBp+z3tOP4LEbkkFkPI2wiBNfumMfVFBnub7PgRsU0agVyButQZuhlYABwZuObdAESd6tajEoxo5Z2oM2CRschD1D3YYf8DkwA9mZSoJwzQ6G5wB+rWPdDXcxxBRN1sRV5FDPQ9H51aoE51s9jgxpp6A+y2ow6tB7ukTnXz88VcgazJef4Ma7MYMoiEDUdd1uTU/R8tU8bc9FvTY/u2fAPxPObwoP9TegAAAABJRU5ErkJggg==',
 'primary_pressed': 'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAABfklEQVR4nO2WvU5UURSF19rnckEhGMKEEiUhFJPYETtM+JnGnjeghjew8A20svAJfACbQUykI3QkUxgSwNJAjERlGO45i+wZJiEUjgN3qPiqU33r7p2Tsy7RRgQoP00vfa1ayBaA9AxqQiLxD0gJHAFghykW29+3XjauO9k9zL74NB6fjL2BuEYLo6ChL5SgFP+A+hB+/X69v/Pq1N3E6sdQ/VF99Dc7/hLy8fnY+glIqTvR/yOCtJBPILZOdx8XlcXGVOOsPf7Tpc232fDkenF+3CJtyCfvw3wdSekiG67kxfnJu6OtlQ3OLNfnEsIegayzrlvLu8inF1AY4nODQi2Ekdx3WILcobs6zlCzSM2A1k5FaVDudLcZdVHSl9+E7rZe9/wuuLvPy94/DwE9eVhRT6z9ng8IUrIk+us5iBC524J4AKWr4inNTXe628BYj7HZumqwMiaRuzrOWLeDz7VvUHof8gnzsrhjiNzhLne6+z4qUwMu/W76gH5bLgE8e+E2D5TPGAAAAABJRU5ErkJggg==',
 'secondary_disabled': 'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAABlklEQVR4nO2WO07DQBCGZyaJsUOCEinimQIaCiQ6OkRBwXXgAFwCqDhDfARERUuHRJEmFIBIQAGB8/BrB/3GFFAQHnbHJ620srzf7I53d8xERKrKzKzo3z48r01ZpS1VWh6PxkTETF+iajs23rryg/BssTFz+cGJDh602+2Z+8fhQf955A18o36kP2oD3yjGwgHXe5Ci67qiqk637502as7Gy8CnKPBNnK7ouyQy4el61d6LzcKmqm67rjtKZn9993i4NFfbffHGATGXkJdvmz+ClITVim3ddJ+OmvP1Pb7u9VZLBeeibFvFNF2/lb+D5OtwHERhPFoX0uJOpVK2jDGUgRwwXHDCLUyyUixIEpUygpk1cZKs4AOHGc38Mwy3TN7nf4FZKGfkP8Ak/lM0EcE9SLmhKvx2e+YRROEWJdOJYoNjndmJVlVOnGQ6QhydeN4wEEk2VBYrUbjghFuas7PtMIyOK2VLUCz+GEThgAtOuKXVahWW5mr73b53jkqU3oIoDvFPWjqG4YALTrhzL/qJPM/flldq5nvY3EaKlwAAAABJRU5ErkJggg==',
 'secondary_focus': 'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAB9UlEQVR4nO2Wv2sUURDHv/Pe2zPrgeCRHCkSVJAUAVMFC4mFRSohXQqx0ZC/QSstLO0EC4uAlY12ASsLC8UiWCmkCBdiuCuSSzglcNnk3o+R2c2eqW7N5a7LFwYeu/M+M294fHcJqZgAYlndfrw/HcXxXfbhevAJQCD0EoOVjkFa/bJJ8mXt7ej6aSbli5sPN65U4uoL52m5fazLgRXOIkUB5Uu+bTSvtJLm89q7qQNhExbf6+mxxfhy0vrcQWVW8x7u3ymFiaphMEC9+wfLuQloNB19/NZRnsZQQuv7YVy5t773IUmTZh/tvppZYn7wbP+4VreB+1StboMwhCVMYdPMcmNK25GfDDarL6/SZFWTc/8654LR0KmTGAPUm54XnvxmAjkfHd1SZRXNtzsjpYW5CAK3LkvUOgtTEN08A8heYQhLmMJWDLrBUHxt3DD/x8x7SfYKI2VBsbDlqlh5J9XPA88lDGGdTM8qcDbGQcBzdVkMOttl70MXBQp1MaJCKVBmN6krDkicswip6UfyLDKDKcIMCOvEJyNF4C1CoO0dR7mXnAdOBKQsBBK2agf7qVw66qx+tanVSnWxa++zcAXRzXNZ58IQljCFrX6sTGxo8m+CHlVPX/+xmw3H/dr1ZsOxMIQlTGEP/ZNJw//oZ30M7bflL/13c6lAr3gzAAAAAElFTkSuQmCC',
 'secondary_hover': 'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAABuklEQVR4nO2Wu0oDURCG/znZ7GbNqnhHKy28EBBEbBUsbGwUwTew1jew8A20svAJIog2aSwE01iICELwUmileEfduNnN6shsjIpFjGvS+cHCKc75hhk4518CAGYmImJZr2/fJAzdHIZCZy7nghiEEjCBYzEDeMWZ6znpyZHmzFenVlykUsd1aOxYsExtprnBiJsx2VSDciACnBxwcx/JpnbsFdydzxPRY+BOJpORlsS06dr2Vl+3NVQbBXQNr0QIOioXZpDnQz3lgcMTe9ewrNHrzKoTtL+Rvl0cSDTOtsTheT6ishkhIALrGvLXWej7mbulieGmOVrbvuqprzEPBnstjQgkcmk5DMyFIszgvSPbf3h2+hWzNtbeFte1SKHNsHJBzopDXOIUt4oAXaZB/NuZl0Jc4hS3YkY+7MxLIU5xK5k7qgQRSKHKqP8CP/E/oh+Ri1axG/wdcctFi1bymSgiTnGrF+DUcTl4RVEhmEHiFLci8jcvLrOe//Lx1P5FDHGIS5ziVlMjrce24y0/elASFsUiYT56DxxxiVPc1Y9MLhn65ck/Q9/N2o4fhP74eE8h9AvVq/fb8gaOYiFnGFNr6QAAAABJRU5ErkJggg==',
 'secondary_normal': 'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAABaUlEQVR4nO2Wv0rDUBTGz7n9GxsqaBed2qWD6O7i6Jv4HA6+gbtP0FdwdBFcBItDpbSDVCqtYElJmzb55LttoYjYiMnWDy4cbu75neS7NzlREREAqqpg3OwOjop55wwi1Ynvc0rld6HoOFzUnQT+3XG18rzOzK6C+1arvO8eXhVymYtdt1gq5LlsR+JqGoh8emb80vNuhl7vUlVHZEuj0cj0+3Bbr6OHEEAYgWI4/+MImctEssgk21ZvtofXvABgCsCWiKJFEMUZi5uyaWSQRab197H9Xi87zlPtwM0u/d7k+SZxL9F58+Yj3z8xKnpe2StZx/F/uKwYZJJtjGotn7MnyJ6ihAQyyTYCmSVgy09Ssk1K8JWUBVKV2RbYpK1FsSxK8g3+LhhRyaVUBGSbCOgEMyTxFV2Xkkm2geB28DEO7GwCT6JLBplkp95wJO2Wqb83/fhaNP3JeDoLbdM/rddt07cbm+ZvyxedO/GSN5tAXwAAAABJRU5ErkJggg==',
 'secondary_pressed': 'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAABzElEQVR4nO3WsUsbYRgG8Od9k7vkCG2N1FioBbs4WIQODi5SOpT+BY7i4qxTKXRwcBDEyU4duohLsX9B6VBKFweHgtTBpdKm0MbWGEs4c2e+R96LgoN4EC+bDxx8y/3e+7473vcEAEiKiNDWK+t/R6n+pAiH46gFEQiuCAl6fgGk7ImLvryYvrtz0cyfL1bXd29HXmWxXPJmh+4FpVIgcMTVukEAVIBmSFR/h82Vd4dv/bi2ICJHiT21sZF7MjAVtPfrnx4/Ko8/6CeCgjgRMA2/WISEhC3qzwPB12/1rdxA+enn/fdhYiyv/VmdGK/MjQ4hOm7Bc0x98EujAhYLiHeq8De3aq9fzgzOy9JabaT/jrf9fKIvn1eI4dIVD9tFUuTEgR82D08OGvGY0vHZ8P1bftEHroNb7F4zzDLTbJWcPCwFOVplZBQV0EyzFQ6xvSBkHJrpEGvad36dmK3ocfSmQFpujig1av0cPQoJKhSeteascTFT4Snb/N4M20kXzQp3hJhptorKx71f/6PjqNOkrOV2G561a7PMNFtfzVR2G43ozY9/UBsW50W6ufRs4Jhlptm9H5nMeOjXm3Ey9OenRzpDv3N2vfttOQUg5zMzPQv0xgAAAABJRU5ErkJggg==',
 'spin_down': 'iVBORw0KGgoAAAANSUhEUgAAABIAAAAKCAYAAAC5Sw6hAAAA7UlEQVR4nGNgwAL+///PiE0cDCByuOXRQX19PRNJFqCD3NyJ7LmVE0VB7NDQVczoBqfVz+TKrGgXhArDDWZCd/Iv3j8iv/7+PJZR2mm7enXY3/r6ehaQIY2Njf+SC3uFGL9/PP//H4sF1CIMV6PYml7e7ZBe1vU2q7zHBiaXWTFNMKOs+056WVcZsloYwPAzzHaQi/4zMG5k/sfo+ZXny0XO79zXGP4zTp/RXdoN8jLItVhdg2YYC9gVpZ326aXdd7Mqeu+ml3WVgMMobSYrQQOwGQZyWWZZdzKyGMkAORxCQ0PhMUgWABlgT4RLAJqmZSkVIbGuAAAAAElFTkSuQmCC',
 'spin_up': 'iVBORw0KGgoAAAANSUhEUgAAABIAAAAKCAYAAAC5Sw6hAAABBklEQVR4nGNgwAP+///PCGPX19czMZADQkNXMYPo9NJO1dSyDiuoYSxkGZJdMVk4vbT7SmZF74f0ki5rfIZhOBfkhdWrw/4mF/YK/fn3/TQDA8M0pr+MTgyMjJszSjttGxsb/9hjMQweBmAAChNGxv/ZFW3Cf/+xnmT4zzBzRndpN0gKZMh/RsYNjP//B8zoLj8MsrCxsfEfpkH//zPWNzQwPv/MK8TI8v8Iw7//82b2lHXV1+8H297Y6PgHbBgD0/r/zP99Z3WUnaivr2dENgzF0Pj8eoG0ki4PcFitgoQVctiklXaapFX2aEBtR/UR9gAPhRuCHH4ENSK7DJshyIYhpy+qAwApc2vFk3zapAAAAABJRU5ErkJggg=='}


_ASSETS.update({'danger_disabled': 'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAABw0lEQVR4nO2WsUoDQRCGZzZrvPMuhxCFGCRGhBSCnZ1ISOEj+AbW+gYWvoFWFj5B7hFERGztBIuAGEUSggbhcsmF3N6NzKpgocaQXJev2uL4ZudnmTkEACAiRETi82u9vi4ta5uIikGvB4CI8BdEZM7N8Wd11e1eLxSLd9+d8utQq9WcxUzmSEi5Z5imJaUEx3HgvyiloA/QfWs2z146nUNE9NgtXdcV1GqZbaUu5nO5zb7vQ0QUx2GoO/ovBIBpw7AM2z6I4niLWq2K67qBbr/x+Hi8VCjs931/AAAzAPB3LL/DlwoN2043n55O8isrB/h8f18yTPPWdhwd1xjyLzhz8j1P9YNgQ6RSqZ2M46SJdCLjyhlkFzvZLQBxVUrJ9pEyHwJpJ+KqIKJwQjf/qZOQO0hC/gEiCkgYMS0wjGlEQxE8uCEpiEggIk/PJIoQu7mDB6XUJKbod1A7iR5EFEXnHc8bfE4MmtDNgZ3sFstra7VBGJ7OWhY/2XDMIsQOdrGT3VitVlO75TKvzMtsPq9XJgHEOGIh4tEGIAzbhnajcZOVsuJeXQU8Un9d+qOgl34QdGOl9NIvlUp66X8En+Bvyzs1pPzraMzf5QAAAABJRU5ErkJggg==',
 'danger_focus': 'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAB3klEQVR4nO2Wv2sUQRTHv29m95I9JaYwhz8axWgh2MmlMAYiqKd9SrERLPwfLPwPLOxsbPMHSCSQA7U6AhaCoLmQNP7gYhFDvM3dzu5X3uwKQTDHkmyXLwz7YOZ95r1h570RACAg4j/A29nW1Vpt7CaAC3uZg1Cn/i8KOW4CNTeHw8G7ufdLn/Yz5a/xutmcmBw7/Yxp9oj9/gnJdAbFtgeoWEMjkHr9t1jzcnvw8+n9TmfHsxcXFuxUrxfZNGqfTLLrOwJMtW5l9XNnSOcgBycAkpAgQP/bD9laWjETBHZDs5raeH6r0Yj9ovaN1vMPM3fYefB4sPv5S0ZmLK+M6qsMZSnTJ7g8e+9KmKYfAQTNVy8kujwt/LWdH1wZaSanJhGvddl5+EQP1iXWXjO1wN4O4r1a4+48oulLHq4pi7XlRhBAfZWhLGUq24C4KBlZP3+WPuqyke9X4a8sZSrbUCTRKSYORyXmLP3DEyNkHvJhIv9XBUvZBhXLHG8wSsdHNFJ60fKCzFF1uYQKlrL1ooXeDn3TOBJJztJeFBoINmhE+l+/i9/5MJkw91eWMpVthi5ddtH4sPemjbi7Ti252miYpuWGc3m57q5TWcpUdvUNZ7HilimVN30fRYXPlj804MT9WmFnoAAAAABJRU5ErkJggg==',
 'danger_hover': 'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAABvElEQVR4nO2WsWsTYRjGn+frfefFoG0IISIqdokgpFNXhw5dsqgBRzdn/Q8c/A90cnBzS6EqSBEcOrg6NSA0i0VLMYSSpvbMed+ZV95LAy4mbZrb+oODb/ju9373fvA+RwAQEZIUXe9tvL1t6d0R8GYUR4CQGAdFAj8AITtOkk9Xa/e+/Ov0RovWxuvL86bwzM/lH+WLxbwNAt0FjNcDeiwSLooQ7u+H7Q/vX/UG3ackD1N3o9GYe1Aq5dq/+5vlW5VluZgHrR3g+ItOjAjFOcNfIdrbrc/lC7mVtU6nn57v27s3z68vLT1GoRDDOaubMQ2kwFqHbtf/vrX14sbd+0+4u75e8ecvNUvVqgeSqXxC2/9L2lKKXkCn2Uzi3s+qGYisLlwp+/A8nEmu6Lvq8DyoU92Gc1y0QSCn7vk4SFGnuo2IuKl7PunSRZxJ+54VJA0yxpwXmMR5iyZidG4gK0TEkLQzHRMjSA0aa+SPfHVRNJyis0KE6lS3MeTHgx/tGEkyGrVnESN1JAnUqW5zrV5vRUdHLxGGJg2LUZFpHh4HThgadao7+8iUGYd+3A/T0K/UHg5Df1g8u9+Wv2vnNDDy6ddpAAAAAElFTkSuQmCC',
 'danger_normal': 'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAABrUlEQVR4nO2WvU4bQRSFz7nYgw3GRRxRpEBOA5IlJARI0FCkyCPkDajhDVLkDUJFwROYR6CgoAEJEAJkCRosCooIp1jsrBmTvdFd24gCrYN/Oj5ppCnufjtzZzVnCQCqSpJq8/vT01LWuTVQi2HzESCIJBSazYwDymro/cHHxcXKS2eqO7k+PMx/yk38GBvPrGfy+Uk4hwlVgMl+dGu8hwRBo355vnNX//OdZBC7y+Xy2LdSKfsA3Z8qFpfjB0QidHb036gSUST2sodq9XgK/LJbqYTx8monxz8/zM1tQMQjitJxcT+QCpEWosj9vrraKiwtb/LX2dFs1uUucjMzKSvpjEFQG/Xb26fQ1+eFT/w6WSi4uI/9rvwl5iBhTnMLKZ/pnL6550mQak5zC4DWENryGuZsSc/vfBAI2g5Giry/oBfvLeqJ2H2OUaFQO4N054Iavh5Ii2p0o95zKBddF1Wa09yiKd1r1Gq+k0yD74RUc5nT3DK9sHLtw3A7Pg8Li7hzir4G0A4cQMxp7tFHpiaE/nOgJ4ufQ78ZBI2/j8049GdXV9uh364Z3W/LP9pzEaEq51F3AAAAAElFTkSuQmCC',
 'danger_pressed': 'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAABvklEQVR4nO2WsUojURSG///qzBjdSBbFRhRtlBUFBYu1WMTCN7FJEfMGFr5BTBFBnyCvYLEsFloIChHFbVZcbDRiMGqcGZkj52rAQuPukOn8YOAWl+/cc+7lnCEAiAhJiq4PS6UJx+AHiJGHMACFRAuEIl2OCwhOwwjbk9ns0WtnZ3OxWyj0fu32Vr10eql3YKDHS6V0E9BSryaAJPxGAzcXF3cnG+ub1/f+Cskb6y6Xyx3zQKp2W/s58m1iVvr7YTwvamb0r6gs8n3DahWnx0d7mS+ZhV9Aw56vUioWxmdmljk0HES+7+hmxICkGM8L5e+Ze7K/vzaVzeV5UCyO9WTSleG5uU4YQ6i8ddnfx5aUgiiSs52dx7tafcoQ0WLf4KBL17VpxpYr1PMJ1WWdiBYNgFG3OyX/W/NWqEud6tYAoS1LuxHrDI2+USQESWoGiWI+A3zEZ4k+xIjtyckgIqJ34NgG1W5onY4G+BPcNxi3Rb+FutSpbiMwW1fn54EEgW1StuXGRcQ61GWdMFtmOpf7/XBbX2f10uiw0NT0WuJ8eBk46lKnupMfmdLmoe/X63bof8/nn4d+M3pSvy1P4Q48x6X45LQAAAAASUVORK5CYII='})


def install(root, family, size):
    size = CONTROL_FONT_SIZE
    style = ttk.Style(root)
    if not hasattr(root, '_control_images'):
        root._control_images = {name: tk.PhotoImage(master=root, data=data)
                                for name, data in _ASSETS.items()}
        images = root._control_images
        for kind in ('secondary', 'primary', 'field', 'danger'):
            style.element_create('Modern.' + kind, 'image', images[kind + '_normal'],
                ('disabled', images[kind + '_disabled']),
                ('pressed', images[kind + '_pressed']),
                ('focus', images[kind + '_focus']),
                ('active', images[kind + '_hover']), border=7, sticky='nsew')
        style.element_create('Modern.chevron', 'image', images['chevron'],
            ('disabled', images['chevron_disabled']),
            ('pressed', images['chevron_active']),
            ('active', images['chevron_active']), sticky='')
        for name in ('card', 'card_tint'):
            style.element_create('Modern.' + name, 'image', images[name], border=13, sticky='nsew')
        style.element_create('Modern.tab', 'image', images['field_disabled'],
            ('selected', images['secondary_normal']), ('active', images['secondary_hover']),
            border=7, sticky='nsew')
        for direction in ('up', 'down'):
            style.element_create('Modern.' + direction + 'arrow', 'image',
                                 images['spin_' + direction], sticky='')
    style.layout('Breadcrumb.TButton', [('Button.padding', {'sticky': 'nsew', 'children': [
        ('Button.focus', {'sticky': 'nsew', 'children': [('Button.label', {'sticky': 'nsew'})]})]})])
    style.configure('Breadcrumb.TButton', font=(family, size), padding=(6, 4),
                    foreground='#68768b', background='#ffffff', anchor='center',
                    focusthickness=1, focuscolor='#315fea')
    style.map('Breadcrumb.TButton', foreground=[('disabled', '#adb7c6'),
                ('selected', '#315fea'), ('active', '#315fea')])
    style.configure('Reference.TNotebook', borderwidth=0, background='#ffffff',
                    bordercolor='#ffffff', lightcolor='#ffffff', darkcolor='#ffffff')
    for name, element in [('Card.TFrame', 'card'), ('Tint.Card.TFrame', 'card_tint')]:
        style.layout(name, [('Modern.' + element, {'sticky': 'nsew'})])
    style.layout('Reference.TNotebook.Tab', [('Modern.tab', {'sticky': 'nsew', 'children': [
        ('Notebook.padding', {'sticky': 'nsew', 'children': [
            ('Notebook.label', {'sticky': 'nsew'})]})]})])
    style.configure('Reference.TNotebook.Tab', padding=(4, 1), font=(family, size), background='#ffffff')
    style.map('Reference.TNotebook.Tab', foreground=[('selected', '#315fea'), ('!selected', '#68768b')])
    style.layout('TEntry', [('Modern.field', {'sticky': 'nsew', 'children': [
        ('Entry.padding', {'sticky': 'nsew', 'children': [('Entry.textarea', {'sticky': 'nsew'})]})]})])
    style.configure('TEntry', padding=(3, 1), background='#ffffff', fieldbackground='#ffffff')
    style.layout('TSpinbox', [('Modern.field', {'sticky': 'nsew', 'children': [
        ('null', {'side': 'right', 'sticky': 'ns', 'children': [
            ('Modern.uparrow', {'side': 'top', 'sticky': 'e'}),
            ('Modern.downarrow', {'side': 'bottom', 'sticky': 'e'})]}),
        ('Spinbox.padding', {'sticky': 'nsew', 'children': [
            ('Spinbox.textarea', {'sticky': 'nsew'})]})]})])
    style.configure('TSpinbox', padding=(3, 1), background='#ffffff', fieldbackground='#ffffff')
    for name, kind, padding in [('TButton', 'secondary', (8, 2)),
                                 ('Primary.TButton', 'primary', (8, 2)),
                                 ('Danger.TButton', 'danger', (8, 2)),
                                 ('Small.TButton', 'secondary', (8, 2))]:
        style.layout(name, [('Modern.' + kind, {'sticky': 'nsew', 'children': [
            ('Button.padding', {'sticky': 'nsew', 'children': [
                ('Button.label', {'sticky': 'nsew'})]})]})])
        primary = kind == 'primary'
        style.configure(name, padding=padding, anchor='center', background='#ffffff',
            foreground='#ffffff' if primary else '#9b434b' if kind == 'danger' else '#243958',
            font=(family, size, 'normal'))
        style.map(name, foreground=[('disabled', '#8c9bb3')])
    style.layout('TCombobox', [('Modern.field', {'sticky': 'nsew', 'children': [
        ('Combobox.padding', {'sticky': 'nsew', 'children': [
            ('Modern.chevron', {'side': 'right', 'sticky': 'ns'}),
            ('Combobox.textarea', {'sticky': 'nsew'})]})]})])
    style.configure('TCombobox', padding=(3, 2), background='#ffffff',
        foreground='#243958', fieldbackground='#ffffff', selectbackground='#ffffff',
        selectforeground='#243958', borderwidth=0)
    style.map('TCombobox', foreground=[('disabled', '#8c9bb3'), ('readonly', '#243958')],
        fieldbackground=[('disabled', '#f2f4f8'), ('readonly', '#ffffff')],
        selectbackground=[('readonly', '#ffffff')], selectforeground=[('readonly', '#243958')])
    for option, value in {'background':'#ffffff', 'foreground':'#243958',
        'selectBackground':'#edf2ff', 'selectForeground':'#315fea',
        'selectBorderWidth':0, 'borderWidth':0, 'highlightThickness':0,
        'font':(family, size), 'relief':'flat'}.items():
        root.option_add('*TCombobox*Listbox.' + option, value)
    root.option_add('*TCombobox*Menu.font', (family, size))


def _surface_style(parent, base):
    try:
        background = parent.cget('background')
    except tk.TclError:
        background = '#ffffff'
    name = 'Surface' + str(background).replace('#', '') + '.' + base
    style = ttk.Style(parent)
    style.configure(name, background=background)
    # State images provide the surface; transparent corners must keep the parent color.
    style.map(name, background=[('disabled', background), ('active', background), ('pressed', background)])
    return name


class Button(ttk.Button):
    def __init__(self, parent, **kwargs):
        kwargs['style'] = _surface_style(parent, kwargs.get('style', 'TButton'))
        kwargs.setdefault('cursor', 'hand2')
        super().__init__(parent, **kwargs)


class Combobox(ttk.Combobox):
    def __init__(self, parent, **kwargs):
        kwargs['style'] = _surface_style(parent, kwargs.get('style', 'TCombobox'))
        kwargs.setdefault('font', (parent._root().family, CONTROL_FONT_SIZE))
        kwargs.setdefault('cursor', 'hand2')
        super().__init__(parent, **kwargs)


class Card(ttk.Frame):
    def __init__(self, parent, *, tint='#ffffff'):
        base = 'Tint.Card.TFrame' if tint == '#edf2ff' else 'Card.TFrame'
        super().__init__(parent, style=_surface_style(parent, base))
