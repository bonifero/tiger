
/Users/cassidal/Documents/vuz/tiger/source/Лаб_3/Загрузка_рюкзака.exe:	file format coff-i386

Disassembly of section CODE:

00401000 <CODE>:
  4609e4: 55                           	pushl	%ebp
  4609e5: 8b ec                        	movl	%esp, %ebp
  4609e7: b9 10 00 00 00               	movl	$0x10, %ecx
  4609ec: 6a 00                        	pushl	$0x0
  4609ee: 6a 00                        	pushl	$0x0
  4609f0: 49                           	decl	%ecx
  4609f1: 75 f9                        	jne	0x4609ec <CODE+0x5f9ec>
  4609f3: 51                           	pushl	%ecx
  4609f4: 53                           	pushl	%ebx
  4609f5: 56                           	pushl	%esi
  4609f6: 57                           	pushl	%edi
  4609f7: 89 45 fc                     	movl	%eax, -0x4(%ebp)
  4609fa: 33 c0                        	xorl	%eax, %eax
  4609fc: 55                           	pushl	%ebp
  4609fd: 68 05 12 46 00               	pushl	$0x461205               # imm = 0x461205
  460a02: 64 ff 30                     	pushl	%fs:(%eax)
  460a05: 64 89 20                     	movl	%esp, %fs:(%eax)
  460a08: c6 45 eb 01                  	movb	$0x1, -0x15(%ebp)
  460a0c: 8b 45 fc                     	movl	-0x4(%ebp), %eax
  460a0f: 8b 80 24 03 00 00            	movl	0x324(%eax), %eax
  460a15: 8b 80 4c 02 00 00            	movl	0x24c(%eax), %eax
  460a1b: 48                           	decl	%eax
  460a1c: 50                           	pushl	%eax
  460a1d: a1 0c 5c 46 00               	movl	0x465c0c, %eax
  460a22: 2b 05 18 5c 46 00            	subl	0x465c18, %eax
  460a28: 8b 15 24 5c 46 00            	movl	0x465c24, %edx
  460a2e: 8d 04 82                     	leal	(%edx,%eax,4), %eax
  460a31: b9 01 00 00 00               	movl	$0x1, %ecx
  460a36: 8b 15 a8 01 46 00            	movl	0x4601a8, %edx
  460a3c: e8 53 44 fa ff               	calll	0x404e94 <CODE+0x3e94>
  460a41: 83 c4 04                     	addl	$0x4, %esp
  460a44: 8b 45 fc                     	movl	-0x4(%ebp), %eax
  460a47: 8b 80 24 03 00 00            	movl	0x324(%eax), %eax
  460a4d: 8b 80 4c 02 00 00            	movl	0x24c(%eax), %eax
  460a53: 48                           	decl	%eax
  460a54: 50                           	pushl	%eax
  460a55: 8d 45 f8                     	leal	-0x8(%ebp), %eax
  460a58: b9 01 00 00 00               	movl	$0x1, %ecx
  460a5d: 8b 15 c4 09 46 00            	movl	0x4609c4, %edx
  460a63: e8 2c 44 fa ff               	calll	0x404e94 <CODE+0x3e94>
  460a68: 83 c4 04                     	addl	$0x4, %esp
  460a6b: 8b 45 fc                     	movl	-0x4(%ebp), %eax
  460a6e: 8b 80 24 03 00 00            	movl	0x324(%eax), %eax
  460a74: 8b 80 4c 02 00 00            	movl	0x24c(%eax), %eax
  460a7a: 48                           	decl	%eax
  460a7b: 50                           	pushl	%eax
  460a7c: 8d 45 f4                     	leal	-0xc(%ebp), %eax
  460a7f: b9 01 00 00 00               	movl	$0x1, %ecx
  460a84: 8b 15 c4 09 46 00            	movl	0x4609c4, %edx
  460a8a: e8 05 44 fa ff               	calll	0x404e94 <CODE+0x3e94>
  460a8f: 83 c4 04                     	addl	$0x4, %esp
  460a92: a1 14 5c 46 00               	movl	0x465c14, %eax
  460a97: 40                           	incl	%eax
  460a98: 50                           	pushl	%eax
  460a99: a1 0c 5c 46 00               	movl	0x465c0c, %eax
  460a9e: 2b 05 18 5c 46 00            	subl	0x465c18, %eax
  460aa4: 8b 15 2c 5c 46 00            	movl	0x465c2c, %edx
  460aaa: 8d 04 82                     	leal	(%edx,%eax,4), %eax
  460aad: b9 01 00 00 00               	movl	$0x1, %ecx
  460ab2: 8b 15 08 02 46 00            	movl	0x460208, %edx
  460ab8: e8 d7 43 fa ff               	calll	0x404e94 <CODE+0x3e94>
  460abd: 83 c4 04                     	addl	$0x4, %esp
  460ac0: a1 14 5c 46 00               	movl	0x465c14, %eax
  460ac5: 40                           	incl	%eax
  460ac6: 50                           	pushl	%eax
  460ac7: a1 0c 5c 46 00               	movl	0x465c0c, %eax
  460acc: 2b 05 18 5c 46 00            	subl	0x465c18, %eax
  460ad2: 8b 15 30 5c 46 00            	movl	0x465c30, %edx
  460ad8: 8d 04 82                     	leal	(%edx,%eax,4), %eax
  460adb: b9 01 00 00 00               	movl	$0x1, %ecx
  460ae0: 8b 15 08 02 46 00            	movl	0x460208, %edx
  460ae6: e8 a9 43 fa ff               	calll	0x404e94 <CODE+0x3e94>
  460aeb: 83 c4 04                     	addl	$0x4, %esp
  460aee: a1 14 5c 46 00               	movl	0x465c14, %eax
  460af3: 85 c0                        	testl	%eax, %eax
  460af5: 0f 8c 9a 03 00 00            	jl	0x460e95 <CODE+0x5fe95>
  460afb: 40                           	incl	%eax
  460afc: 89 45 e4                     	movl	%eax, -0x1c(%ebp)
  460aff: 33 f6                        	xorl	%esi, %esi
  460b01: 8b 45 fc                     	movl	-0x4(%ebp), %eax
  460b04: 8b 80 24 03 00 00            	movl	0x324(%eax), %eax
  460b0a: 8b 80 1c 02 00 00            	movl	0x21c(%eax), %eax
  460b10: 48                           	decl	%eax
  460b11: 50                           	pushl	%eax
  460b12: 8b 45 f8                     	movl	-0x8(%ebp), %eax
  460b15: 8d 04 b0                     	leal	(%eax,%esi,4), %eax
  460b18: b9 01 00 00 00               	movl	$0x1, %ecx
  460b1d: 8b 15 a4 09 46 00            	movl	0x4609a4, %edx
  460b23: e8 6c 43 fa ff               	calll	0x404e94 <CODE+0x3e94>
  460b28: 83 c4 04                     	addl	$0x4, %esp
  460b2b: 8b 45 fc                     	movl	-0x4(%ebp), %eax
  460b2e: 8b 80 24 03 00 00            	movl	0x324(%eax), %eax
  460b34: 8b 80 1c 02 00 00            	movl	0x21c(%eax), %eax
  460b3a: 48                           	decl	%eax
  460b3b: 50                           	pushl	%eax
  460b3c: 8b 45 f4                     	movl	-0xc(%ebp), %eax
  460b3f: 8d 04 b0                     	leal	(%eax,%esi,4), %eax
  460b42: b9 01 00 00 00               	movl	$0x1, %ecx
  460b47: 8b 15 a4 09 46 00            	movl	0x4609a4, %edx
  460b4d: e8 42 43 fa ff               	calll	0x404e94 <CODE+0x3e94>
  460b52: 83 c4 04                     	addl	$0x4, %esp
  460b55: 8b 45 fc                     	movl	-0x4(%ebp), %eax
  460b58: 8b 80 24 03 00 00            	movl	0x324(%eax), %eax
  460b5e: 8b 80 1c 02 00 00            	movl	0x21c(%eax), %eax
  460b64: 48                           	decl	%eax
  460b65: 50                           	pushl	%eax
  460b66: a1 0c 5c 46 00               	movl	0x465c0c, %eax
  460b6b: 2b 05 18 5c 46 00            	subl	0x465c18, %eax
  460b71: 8b 15 24 5c 46 00            	movl	0x465c24, %edx
  460b77: 8b 04 82                     	movl	(%edx,%eax,4), %eax
  460b7a: 8d 04 b0                     	leal	(%eax,%esi,4), %eax
  460b7d: b9 01 00 00 00               	movl	$0x1, %ecx
  460b82: 8b 15 88 01 46 00            	movl	0x460188, %edx
  460b88: e8 07 43 fa ff               	calll	0x404e94 <CODE+0x3e94>
  460b8d: 83 c4 04                     	addl	$0x4, %esp
  460b90: 83 3d 18 5c 46 00 01         	cmpl	$0x1, 0x465c18
  460b97: 75 69                        	jne	0x460c02 <CODE+0x5fc02>
  460b99: 85 f6                        	testl	%esi, %esi
  460b9b: 7e 65                        	jle	0x460c02 <CODE+0x5fc02>
  460b9d: 8b 45 fc                     	movl	-0x4(%ebp), %eax
  460ba0: 8b 80 24 03 00 00            	movl	0x324(%eax), %eax
  460ba6: 8b 80 1c 02 00 00            	movl	0x21c(%eax), %eax
  460bac: 83 e8 02                     	subl	$0x2, %eax
  460baf: 85 c0                        	testl	%eax, %eax
  460bb1: 0f 8c de 02 00 00            	jl	0x460e95 <CODE+0x5fe95>
  460bb7: 40                           	incl	%eax
  460bb8: 89 45 e0                     	movl	%eax, -0x20(%ebp)
  460bbb: 33 db                        	xorl	%ebx, %ebx
  460bbd: 8d 45 dc                     	leal	-0x24(%ebp), %eax
  460bc0: 50                           	pushl	%eax
  460bc1: 8d 53 01                     	leal	0x1(%ebx), %edx
  460bc4: 8b 45 fc                     	movl	-0x4(%ebp), %eax
  460bc7: 8b 80 24 03 00 00            	movl	0x324(%eax), %eax
  460bcd: b9 01 00 00 00               	movl	$0x1, %ecx
  460bd2: e8 9d f0 ff ff               	calll	0x45fc74 <CODE+0x5ec74>
  460bd7: 8b 45 dc                     	movl	-0x24(%ebp), %eax
  460bda: e8 2d 73 fa ff               	calll	0x407f0c <CODE+0x6f0c>
  460bdf: 8b f8                        	movl	%eax, %edi
  460be1: 8b 45 f4                     	movl	-0xc(%ebp), %eax
  460be4: 8b 00                        	movl	(%eax), %eax
  460be6: 89 3c 98                     	movl	%edi, (%eax,%ebx,4)
  460be9: 8b 45 f8                     	movl	-0x8(%ebp), %eax
  460bec: 8b 00                        	movl	(%eax), %eax
  460bee: 3b 3c 98                     	cmpl	(%eax,%ebx,4), %edi
  460bf1: 74 04                        	je	0x460bf7 <CODE+0x5fbf7>
  460bf3: c6 45 eb 00                  	movb	$0x0, -0x15(%ebp)
  460bf7: 43                           	incl	%ebx
  460bf8: ff 4d e0                     	decl	-0x20(%ebp)
  460bfb: 75 c0                        	jne	0x460bbd <CODE+0x5fbbd>
  460bfd: e9 93 02 00 00               	jmp	0x460e95 <CODE+0x5fe95>
  460c02: c7 45 f0 ff ff ff ff         	movl	$0xffffffff, -0x10(%ebp) # imm = 0xFFFFFFFF
  460c09: 8d 45 d8                     	leal	-0x28(%ebp), %eax
  460c0c: 50                           	pushl	%eax
  460c0d: 8b 45 fc                     	movl	-0x4(%ebp), %eax
  460c10: 8b 80 fc 02 00 00            	movl	0x2fc(%eax), %eax
  460c16: 8b 0d 18 5c 46 00            	movl	0x465c18, %ecx
  460c1c: 33 d2                        	xorl	%edx, %edx
  460c1e: e8 51 f0 ff ff               	calll	0x45fc74 <CODE+0x5ec74>
  460c23: 8b 45 d8                     	movl	-0x28(%ebp), %eax
  460c26: e8 e1 72 fa ff               	calll	0x407f0c <CODE+0x6f0c>
  460c2b: 89 45 d4                     	movl	%eax, -0x2c(%ebp)
  460c2e: db 45 d4                     	fildl	-0x2c(%ebp)
  460c31: a1 14 5c 46 00               	movl	0x465c14, %eax
  460c36: 2b c6                        	subl	%esi, %eax
  460c38: 89 45 d0                     	movl	%eax, -0x30(%ebp)
  460c3b: db 45 d0                     	fildl	-0x30(%ebp)
  460c3e: de f1                        	fdivp	%st, %st(1)
  460c40: e8 d7 1c fa ff               	calll	0x40291c <CODE+0x191c>
  460c45: e8 f2 1c fa ff               	calll	0x40293c <CODE+0x193c>
  460c4a: 52                           	pushl	%edx
  460c4b: 50                           	pushl	%eax
  460c4c: a1 0c 5c 46 00               	movl	0x465c0c, %eax
  460c51: 99                           	cltd
  460c52: 3b 54 24 04                  	cmpl	0x4(%esp), %edx
  460c56: 75 09                        	jne	0x460c61 <CODE+0x5fc61>
  460c58: 3b 04 24                     	cmpl	(%esp), %eax
  460c5b: 5a                           	popl	%edx
  460c5c: 58                           	popl	%eax
  460c5d: 73 0d                        	jae	0x460c6c <CODE+0x5fc6c>
  460c5f: eb 04                        	jmp	0x460c65 <CODE+0x5fc65>
  460c61: 5a                           	popl	%edx
  460c62: 58                           	popl	%eax
  460c63: 7d 07                        	jge	0x460c6c <CODE+0x5fc6c>
  460c65: a1 0c 5c 46 00               	movl	0x465c0c, %eax
  460c6a: eb 41                        	jmp	0x460cad <CODE+0x5fcad>
  460c6c: 8d 45 cc                     	leal	-0x34(%ebp), %eax
  460c6f: 50                           	pushl	%eax
  460c70: 8b 45 fc                     	movl	-0x4(%ebp), %eax
  460c73: 8b 80 fc 02 00 00            	movl	0x2fc(%eax), %eax
  460c79: 8b 0d 18 5c 46 00            	movl	0x465c18, %ecx
  460c7f: 33 d2                        	xorl	%edx, %edx
  460c81: e8 ee ef ff ff               	calll	0x45fc74 <CODE+0x5ec74>
  460c86: 8b 45 cc                     	movl	-0x34(%ebp), %eax
  460c89: e8 7e 72 fa ff               	calll	0x407f0c <CODE+0x6f0c>
  460c8e: 89 45 d4                     	movl	%eax, -0x2c(%ebp)
  460c91: db 45 d4                     	fildl	-0x2c(%ebp)
  460c94: a1 14 5c 46 00               	movl	0x465c14, %eax
  460c99: 2b c6                        	subl	%esi, %eax
  460c9b: 89 45 d0                     	movl	%eax, -0x30(%ebp)
  460c9e: db 45 d0                     	fildl	-0x30(%ebp)
  460ca1: de f1                        	fdivp	%st, %st(1)
  460ca3: e8 74 1c fa ff               	calll	0x40291c <CODE+0x191c>
  460ca8: e8 8f 1c fa ff               	calll	0x40293c <CODE+0x193c>
  460cad: 85 c0                        	testl	%eax, %eax
  460caf: 0f 8c 98 01 00 00            	jl	0x460e4d <CODE+0x5fe4d>
  460cb5: 40                           	incl	%eax
  460cb6: 89 45 e0                     	movl	%eax, -0x20(%ebp)
  460cb9: 33 db                        	xorl	%ebx, %ebx
  460cbb: a1 18 5c 46 00               	movl	0x465c18, %eax
  460cc0: 3b 05 0c 5c 46 00            	cmpl	0x465c0c, %eax
  460cc6: 75 70                        	jne	0x460d38 <CODE+0x5fd38>
  460cc8: 8d 45 c8                     	leal	-0x38(%ebp), %eax
  460ccb: 50                           	pushl	%eax
  460ccc: 8d 7b 01                     	leal	0x1(%ebx), %edi
  460ccf: 8b d7                        	movl	%edi, %edx
  460cd1: 8b 45 fc                     	movl	-0x4(%ebp), %eax
  460cd4: 8b 80 f8 02 00 00            	movl	0x2f8(%eax), %eax
  460cda: 8b 0d 18 5c 46 00            	movl	0x465c18, %ecx
  460ce0: e8 8f ef ff ff               	calll	0x45fc74 <CODE+0x5ec74>
  460ce5: 8b 45 c8                     	movl	-0x38(%ebp), %eax
  460ce8: e8 1f 72 fa ff               	calll	0x407f0c <CODE+0x6f0c>
  460ced: 8b 55 f8                     	movl	-0x8(%ebp), %edx
  460cf0: 8b 14 b2                     	movl	(%edx,%esi,4), %edx
  460cf3: 89 04 9a                     	movl	%eax, (%edx,%ebx,4)
  460cf6: 8d 45 c4                     	leal	-0x3c(%ebp), %eax
  460cf9: 50                           	pushl	%eax
  460cfa: 8b d7                        	movl	%edi, %edx
  460cfc: 8b 45 fc                     	movl	-0x4(%ebp), %eax
  460cff: 8b 80 f8 02 00 00            	movl	0x2f8(%eax), %eax
  460d05: 8b 0d 18 5c 46 00            	movl	0x465c18, %ecx
  460d0b: e8 64 ef ff ff               	calll	0x45fc74 <CODE+0x5ec74>
  460d10: 8b 45 c4                     	movl	-0x3c(%ebp), %eax
  460d13: e8 f4 71 fa ff               	calll	0x407f0c <CODE+0x6f0c>
  460d18: 8b 15 0c 5c 46 00            	movl	0x465c0c, %edx
  460d1e: 2b 15 18 5c 46 00            	subl	0x465c18, %edx
  460d24: 8b 0d 24 5c 46 00            	movl	0x465c24, %ecx
  460d2a: 8b 14 91                     	movl	(%ecx,%edx,4), %edx
  460d2d: 8b 14 b2                     	movl	(%edx,%esi,4), %edx
  460d30: 89 04 9a                     	movl	%eax, (%edx,%ebx,4)
  460d33: e9 eb 00 00 00               	jmp	0x460e23 <CODE+0x5fe23>
  460d38: 8d 45 c0                     	leal	-0x40(%ebp), %eax
  460d3b: 50                           	pushl	%eax
  460d3c: 8d 53 01                     	leal	0x1(%ebx), %edx
  460d3f: 8b 45 fc                     	movl	-0x4(%ebp), %eax
  460d42: 8b 80 f8 02 00 00            	movl	0x2f8(%eax), %eax
  460d48: 8b 0d 18 5c 46 00            	movl	0x465c18, %ecx
  460d4e: e8 21 ef ff ff               	calll	0x45fc74 <CODE+0x5ec74>
  460d53: 8b 45 c0                     	movl	-0x40(%ebp), %eax
  460d56: e8 b1 71 fa ff               	calll	0x407f0c <CODE+0x6f0c>
  460d5b: 8b f8                        	movl	%eax, %edi
  460d5d: 8d 45 bc                     	leal	-0x44(%ebp), %eax
  460d60: 50                           	pushl	%eax
  460d61: 8b 45 fc                     	movl	-0x4(%ebp), %eax
  460d64: 8b 80 fc 02 00 00            	movl	0x2fc(%eax), %eax
  460d6a: 8b 0d 18 5c 46 00            	movl	0x465c18, %ecx
  460d70: 33 d2                        	xorl	%edx, %edx
  460d72: e8 fd ee ff ff               	calll	0x45fc74 <CODE+0x5ec74>
  460d77: 8b 45 bc                     	movl	-0x44(%ebp), %eax
  460d7a: e8 8d 71 fa ff               	calll	0x407f0c <CODE+0x6f0c>
  460d7f: f7 eb                        	imull	%ebx
  460d81: 03 c6                        	addl	%esi, %eax
  460d83: 8b 15 0c 5c 46 00            	movl	0x465c0c, %edx
  460d89: 2b 15 18 5c 46 00            	subl	0x465c18, %edx
  460d8f: 8b 0d 2c 5c 46 00            	movl	0x465c2c, %ecx
  460d95: 8b 54 91 fc                  	movl	-0x4(%ecx,%edx,4), %edx
  460d99: 03 3c 82                     	addl	(%edx,%eax,4), %edi
  460d9c: a1 0c 5c 46 00               	movl	0x465c0c, %eax
  460da1: 2b 05 18 5c 46 00            	subl	0x465c18, %eax
  460da7: 8b 15 24 5c 46 00            	movl	0x465c24, %edx
  460dad: 8b 04 82                     	movl	(%edx,%eax,4), %eax
  460db0: 8b 04 b0                     	movl	(%eax,%esi,4), %eax
  460db3: 89 3c 98                     	movl	%edi, (%eax,%ebx,4)
  460db6: 8d 45 b8                     	leal	-0x48(%ebp), %eax
  460db9: 50                           	pushl	%eax
  460dba: 8d 53 01                     	leal	0x1(%ebx), %edx
  460dbd: 8b 45 fc                     	movl	-0x4(%ebp), %eax
  460dc0: 8b 80 f8 02 00 00            	movl	0x2f8(%eax), %eax
  460dc6: 8b 0d 18 5c 46 00            	movl	0x465c18, %ecx
  460dcc: e8 a3 ee ff ff               	calll	0x45fc74 <CODE+0x5ec74>
  460dd1: 8b 45 b8                     	movl	-0x48(%ebp), %eax
  460dd4: e8 33 71 fa ff               	calll	0x407f0c <CODE+0x6f0c>
  460dd9: 8b f8                        	movl	%eax, %edi
  460ddb: 8d 45 b4                     	leal	-0x4c(%ebp), %eax
  460dde: 50                           	pushl	%eax
  460ddf: 8b 45 fc                     	movl	-0x4(%ebp), %eax
  460de2: 8b 80 fc 02 00 00            	movl	0x2fc(%eax), %eax
  460de8: 8b 0d 18 5c 46 00            	movl	0x465c18, %ecx
  460dee: 33 d2                        	xorl	%edx, %edx
  460df0: e8 7f ee ff ff               	calll	0x45fc74 <CODE+0x5ec74>
  460df5: 8b 45 b4                     	movl	-0x4c(%ebp), %eax
  460df8: e8 0f 71 fa ff               	calll	0x407f0c <CODE+0x6f0c>
  460dfd: f7 eb                        	imull	%ebx
  460dff: 03 c6                        	addl	%esi, %eax
  460e01: 8b 15 0c 5c 46 00            	movl	0x465c0c, %edx
  460e07: 2b 15 18 5c 46 00            	subl	0x465c18, %edx
  460e0d: 8b 0d 2c 5c 46 00            	movl	0x465c2c, %ecx
  460e13: 8b 54 91 fc                  	movl	-0x4(%ecx,%edx,4), %edx
  460e17: 03 3c 82                     	addl	(%edx,%eax,4), %edi
  460e1a: 8b 45 f8                     	movl	-0x8(%ebp), %eax
  460e1d: 8b 04 b0                     	movl	(%eax,%esi,4), %eax
  460e20: 89 3c 98                     	movl	%edi, (%eax,%ebx,4)
  460e23: 83 7d f0 ff                  	cmpl	$-0x1, -0x10(%ebp)
  460e27: 74 17                        	je	0x460e40 <CODE+0x5fe40>
  460e29: 8b 45 f8                     	movl	-0x8(%ebp), %eax
  460e2c: 8b 04 b0                     	movl	(%eax,%esi,4), %eax
  460e2f: 8b 55 f0                     	movl	-0x10(%ebp), %edx
  460e32: 8b 04 90                     	movl	(%eax,%edx,4), %eax
  460e35: 8b 55 f8                     	movl	-0x8(%ebp), %edx
  460e38: 8b 14 b2                     	movl	(%edx,%esi,4), %edx
  460e3b: 3b 04 9a                     	cmpl	(%edx,%ebx,4), %eax
  460e3e: 7d 03                        	jge	0x460e43 <CODE+0x5fe43>
  460e40: 89 5d f0                     	movl	%ebx, -0x10(%ebp)
  460e43: 43                           	incl	%ebx
  460e44: ff 4d e0                     	decl	-0x20(%ebp)
  460e47: 0f 85 6e fe ff ff            	jne	0x460cbb <CODE+0x5fcbb>
  460e4d: a1 0c 5c 46 00               	movl	0x465c0c, %eax
  460e52: 2b 05 18 5c 46 00            	subl	0x465c18, %eax
  460e58: 8b 15 30 5c 46 00            	movl	0x465c30, %edx
  460e5e: 8b 04 82                     	movl	(%edx,%eax,4), %eax
  460e61: 8b 55 f0                     	movl	-0x10(%ebp), %edx
  460e64: 89 14 b0                     	movl	%edx, (%eax,%esi,4)
  460e67: 8b 45 f8                     	movl	-0x8(%ebp), %eax
  460e6a: 8b 04 b0                     	movl	(%eax,%esi,4), %eax
  460e6d: 8b 55 f0                     	movl	-0x10(%ebp), %edx
  460e70: 8b 04 90                     	movl	(%eax,%edx,4), %eax
  460e73: 8b 15 0c 5c 46 00            	movl	0x465c0c, %edx
  460e79: 2b 15 18 5c 46 00            	subl	0x465c18, %edx
  460e7f: 8b 0d 2c 5c 46 00            	movl	0x465c2c, %ecx
  460e85: 8b 14 91                     	movl	(%ecx,%edx,4), %edx
  460e88: 89 04 b2                     	movl	%eax, (%edx,%esi,4)
  460e8b: 46                           	incl	%esi
  460e8c: ff 4d e4                     	decl	-0x1c(%ebp)
  460e8f: 0f 85 6c fc ff ff            	jne	0x460b01 <CODE+0x5fb01>
  460e95: 83 3d 18 5c 46 00 01         	cmpl	$0x1, 0x465c18
  460e9c: 0f 84 de 00 00 00            	je	0x460f80 <CODE+0x5ff80>
  460ea2: 8b 45 fc                     	movl	-0x4(%ebp), %eax
  460ea5: 8b 80 24 03 00 00            	movl	0x324(%eax), %eax
  460eab: 8b 90 4c 02 00 00            	movl	0x24c(%eax), %edx
  460eb1: 89 55 ec                     	movl	%edx, -0x14(%ebp)
  460eb4: 8b b8 1c 02 00 00            	movl	0x21c(%eax), %edi
  460eba: 8b 45 ec                     	movl	-0x14(%ebp), %eax
  460ebd: 48                           	decl	%eax
  460ebe: 85 c0                        	testl	%eax, %eax
  460ec0: 7e 77                        	jle	0x460f39 <CODE+0x5ff39>
  460ec2: 89 45 e4                     	movl	%eax, -0x1c(%ebp)
  460ec5: be 01 00 00 00               	movl	$0x1, %esi
  460eca: 8b c7                        	movl	%edi, %eax
  460ecc: 48                           	decl	%eax
  460ecd: 85 c0                        	testl	%eax, %eax
  460ecf: 7e 62                        	jle	0x460f33 <CODE+0x5ff33>
  460ed1: 89 45 e0                     	movl	%eax, -0x20(%ebp)
  460ed4: bb 01 00 00 00               	movl	$0x1, %ebx
  460ed9: 8d 45 b0                     	leal	-0x50(%ebp), %eax
  460edc: 50                           	pushl	%eax
  460edd: 8b 45 fc                     	movl	-0x4(%ebp), %eax
  460ee0: 8b 80 24 03 00 00            	movl	0x324(%eax), %eax
  460ee6: 8b ce                        	movl	%esi, %ecx
  460ee8: 8b d3                        	movl	%ebx, %edx
  460eea: e8 85 ed ff ff               	calll	0x45fc74 <CODE+0x5ec74>
  460eef: 83 7d b0 00                  	cmpl	$0x0, -0x50(%ebp)
  460ef3: 75 0f                        	jne	0x460f04 <CODE+0x5ff04>
  460ef5: 8b 45 f4                     	movl	-0xc(%ebp), %eax
  460ef8: 8b 44 b0 fc                  	movl	-0x4(%eax,%esi,4), %eax
  460efc: 33 d2                        	xorl	%edx, %edx
  460efe: 89 54 98 fc                  	movl	%edx, -0x4(%eax,%ebx,4)
  460f02: eb 29                        	jmp	0x460f2d <CODE+0x5ff2d>
  460f04: 8d 45 ac                     	leal	-0x54(%ebp), %eax
  460f07: 50                           	pushl	%eax
  460f08: 8b 45 fc                     	movl	-0x4(%ebp), %eax
  460f0b: 8b 80 24 03 00 00            	movl	0x324(%eax), %eax
  460f11: 8b ce                        	movl	%esi, %ecx
  460f13: 8b d3                        	movl	%ebx, %edx
  460f15: e8 5a ed ff ff               	calll	0x45fc74 <CODE+0x5ec74>
  460f1a: 8b 45 ac                     	movl	-0x54(%ebp), %eax
  460f1d: e8 ea 6f fa ff               	calll	0x407f0c <CODE+0x6f0c>
  460f22: 8b 55 f4                     	movl	-0xc(%ebp), %edx
  460f25: 8b 54 b2 fc                  	movl	-0x4(%edx,%esi,4), %edx
  460f29: 89 44 9a fc                  	movl	%eax, -0x4(%edx,%ebx,4)
  460f2d: 43                           	incl	%ebx
  460f2e: ff 4d e0                     	decl	-0x20(%ebp)
  460f31: 75 a6                        	jne	0x460ed9 <CODE+0x5fed9>
  460f33: 46                           	incl	%esi
  460f34: ff 4d e4                     	decl	-0x1c(%ebp)
  460f37: 75 91                        	jne	0x460eca <CODE+0x5feca>
  460f39: 8b 45 ec                     	movl	-0x14(%ebp), %eax
  460f3c: 48                           	decl	%eax
  460f3d: 85 c0                        	testl	%eax, %eax
  460f3f: 7e 3f                        	jle	0x460f80 <CODE+0x5ff80>
  460f41: 89 45 e4                     	movl	%eax, -0x1c(%ebp)
  460f44: be 01 00 00 00               	movl	$0x1, %esi
  460f49: 8b c7                        	movl	%edi, %eax
  460f4b: 48                           	decl	%eax
  460f4c: 85 c0                        	testl	%eax, %eax
  460f4e: 7e 2a                        	jle	0x460f7a <CODE+0x5ff7a>
  460f50: 89 45 e0                     	movl	%eax, -0x20(%ebp)
  460f53: bb 01 00 00 00               	movl	$0x1, %ebx
  460f58: 8b 45 f8                     	movl	-0x8(%ebp), %eax
  460f5b: 8b 44 b0 fc                  	movl	-0x4(%eax,%esi,4), %eax
  460f5f: 8b 44 98 fc                  	movl	-0x4(%eax,%ebx,4), %eax
  460f63: 8b 55 f4                     	movl	-0xc(%ebp), %edx
  460f66: 8b 54 b2 fc                  	movl	-0x4(%edx,%esi,4), %edx
  460f6a: 3b 44 9a fc                  	cmpl	-0x4(%edx,%ebx,4), %eax
  460f6e: 74 04                        	je	0x460f74 <CODE+0x5ff74>
  460f70: c6 45 eb 00                  	movb	$0x0, -0x15(%ebp)
  460f74: 43                           	incl	%ebx
  460f75: ff 4d e0                     	decl	-0x20(%ebp)
  460f78: 75 de                        	jne	0x460f58 <CODE+0x5ff58>
  460f7a: 46                           	incl	%esi
  460f7b: ff 4d e4                     	decl	-0x1c(%ebp)
  460f7e: 75 c9                        	jne	0x460f49 <CODE+0x5ff49>
  460f80: 80 7d eb 00                  	cmpb	$0x0, -0x15(%ebp)
  460f84: 0f 84 2d 02 00 00            	je	0x4611b7 <CODE+0x601b7>
  460f8a: b8 1c 12 46 00               	movl	$0x46121c, %eax         # imm = 0x46121C
  460f8f: e8 98 67 fc ff               	calll	0x42772c <CODE+0x2672c>
  460f94: 8b 45 fc                     	movl	-0x4(%ebp), %eax
  460f97: 8b 80 44 03 00 00            	movl	0x344(%eax), %eax
  460f9d: b2 01                        	movb	$0x1, %dl
  460f9f: e8 fc 23 fd ff               	calll	0x4333a0 <CODE+0x323a0>
  460fa4: 68 30 12 46 00               	pushl	$0x461230               # imm = 0x461230
  460fa9: 8d 55 a4                     	leal	-0x5c(%ebp), %edx
  460fac: a1 0c 5c 46 00               	movl	0x465c0c, %eax
  460fb1: 2b 05 18 5c 46 00            	subl	0x465c18, %eax
  460fb7: 40                           	incl	%eax
  460fb8: e8 13 6e fa ff               	calll	0x407dd0 <CODE+0x6dd0>
  460fbd: ff 75 a4                     	pushl	-0x5c(%ebp)
  460fc0: 68 48 12 46 00               	pushl	$0x461248               # imm = 0x461248
  460fc5: 8d 55 a0                     	leal	-0x60(%ebp), %edx
  460fc8: a1 18 5c 46 00               	movl	0x465c18, %eax
  460fcd: e8 fe 6d fa ff               	calll	0x407dd0 <CODE+0x6dd0>
  460fd2: ff 75 a0                     	pushl	-0x60(%ebp)
  460fd5: 68 58 12 46 00               	pushl	$0x461258               # imm = 0x461258
  460fda: 8d 45 a8                     	leal	-0x58(%ebp), %eax
  460fdd: ba 05 00 00 00               	movl	$0x5, %edx
  460fe2: e8 4d 32 fa ff               	calll	0x404234 <CODE+0x3234>
  460fe7: 8b 55 a8                     	movl	-0x58(%ebp), %edx
  460fea: 8b 45 fc                     	movl	-0x4(%ebp), %eax
  460fed: 8b 80 44 03 00 00            	movl	0x344(%eax), %eax
  460ff3: e8 b8 24 fd ff               	calll	0x4334b0 <CODE+0x324b0>
  460ff8: 8b 45 fc                     	movl	-0x4(%ebp), %eax
  460ffb: 8b 80 38 03 00 00            	movl	0x338(%eax), %eax
  461001: b2 01                        	movb	$0x1, %dl
  461003: e8 98 23 fd ff               	calll	0x4333a0 <CODE+0x323a0>
  461008: 8b 45 fc                     	movl	-0x4(%ebp), %eax
  46100b: 8b 80 28 03 00 00            	movl	0x328(%eax), %eax
  461011: b2 01                        	movb	$0x1, %dl
  461013: e8 88 23 fd ff               	calll	0x4333a0 <CODE+0x323a0>
  461018: 33 f6                        	xorl	%esi, %esi
  46101a: 8b 45 fc                     	movl	-0x4(%ebp), %eax
  46101d: 8b 80 28 03 00 00            	movl	0x328(%eax), %eax
  461023: 8b 80 4c 02 00 00            	movl	0x24c(%eax), %eax
  461029: 48                           	decl	%eax
  46102a: 85 c0                        	testl	%eax, %eax
  46102c: 7c 21                        	jl	0x46104f <CODE+0x6004f>
  46102e: 40                           	incl	%eax
  46102f: 89 45 e4                     	movl	%eax, -0x1c(%ebp)
  461032: 33 db                        	xorl	%ebx, %ebx
  461034: 6a 00                        	pushl	$0x0
  461036: 8d 4b 01                     	leal	0x1(%ebx), %ecx
  461039: 8b 45 fc                     	movl	-0x4(%ebp), %eax
  46103c: 8b 80 28 03 00 00            	movl	0x328(%eax), %eax
  461042: 8b d6                        	movl	%esi, %edx
  461044: e8 9b ec ff ff               	calll	0x45fce4 <CODE+0x5ece4>
  461049: 43                           	incl	%ebx
  46104a: ff 4d e4                     	decl	-0x1c(%ebp)
  46104d: 75 e5                        	jne	0x461034 <CODE+0x60034>
  46104f: 46                           	incl	%esi
  461050: 83 fe 02                     	cmpl	$0x2, %esi
  461053: 75 c5                        	jne	0x46101a <CODE+0x6001a>
  461055: 8b 45 fc                     	movl	-0x4(%ebp), %eax
  461058: 8b 80 00 03 00 00            	movl	0x300(%eax), %eax
  46105e: 33 d2                        	xorl	%edx, %edx
  461060: e8 3b 23 fd ff               	calll	0x4333a0 <CODE+0x323a0>
  461065: 8b 45 fc                     	movl	-0x4(%ebp), %eax
  461068: 8b 80 14 03 00 00            	movl	0x314(%eax), %eax
  46106e: ba 64 12 46 00               	movl	$0x461264, %edx         # imm = 0x461264
  461073: e8 38 24 fd ff               	calll	0x4334b0 <CODE+0x324b0>
  461078: 8b 45 fc                     	movl	-0x4(%ebp), %eax
  46107b: 8b 80 48 03 00 00            	movl	0x348(%eax), %eax
  461081: b2 01                        	movb	$0x1, %dl
  461083: e8 18 23 fd ff               	calll	0x4333a0 <CODE+0x323a0>
  461088: 68 a0 12 46 00               	pushl	$0x4612a0               # imm = 0x4612A0
  46108d: 8d 55 98                     	leal	-0x68(%ebp), %edx
  461090: a1 18 5c 46 00               	movl	0x465c18, %eax
  461095: e8 36 6d fa ff               	calll	0x407dd0 <CODE+0x6dd0>
  46109a: ff 75 98                     	pushl	-0x68(%ebp)
  46109d: 68 ac 12 46 00               	pushl	$0x4612ac               # imm = 0x4612AC
  4610a2: 68 b8 12 46 00               	pushl	$0x4612b8               # imm = 0x4612B8
  4610a7: 68 c4 12 46 00               	pushl	$0x4612c4               # imm = 0x4612C4
  4610ac: 68 b8 12 46 00               	pushl	$0x4612b8               # imm = 0x4612B8
  4610b1: 68 d0 12 46 00               	pushl	$0x4612d0               # imm = 0x4612D0
  4610b6: 68 b8 12 46 00               	pushl	$0x4612b8               # imm = 0x4612B8
  4610bb: 68 e4 12 46 00               	pushl	$0x4612e4               # imm = 0x4612E4
  4610c0: 8d 55 94                     	leal	-0x6c(%ebp), %edx
  4610c3: a1 18 5c 46 00               	movl	0x465c18, %eax
  4610c8: e8 03 6d fa ff               	calll	0x407dd0 <CODE+0x6dd0>
  4610cd: ff 75 94                     	pushl	-0x6c(%ebp)
  4610d0: 68 f0 12 46 00               	pushl	$0x4612f0               # imm = 0x4612F0
  4610d5: 8d 55 90                     	leal	-0x70(%ebp), %edx
  4610d8: a1 18 5c 46 00               	movl	0x465c18, %eax
  4610dd: e8 ee 6c fa ff               	calll	0x407dd0 <CODE+0x6dd0>
  4610e2: ff 75 90                     	pushl	-0x70(%ebp)
  4610e5: 68 fc 12 46 00               	pushl	$0x4612fc               # imm = 0x4612FC
  4610ea: 68 08 13 46 00               	pushl	$0x461308               # imm = 0x461308
  4610ef: 8d 45 9c                     	leal	-0x64(%ebp), %eax
  4610f2: ba 0e 00 00 00               	movl	$0xe, %edx
  4610f7: e8 38 31 fa ff               	calll	0x404234 <CODE+0x3234>
  4610fc: 8b 55 9c                     	movl	-0x64(%ebp), %edx
  4610ff: 8b 45 fc                     	movl	-0x4(%ebp), %eax
  461102: 8b 80 48 03 00 00            	movl	0x348(%eax), %eax
  461108: e8 a3 23 fd ff               	calll	0x4334b0 <CODE+0x324b0>
  46110d: 8b 45 fc                     	movl	-0x4(%ebp), %eax
  461110: 8b 80 34 03 00 00            	movl	0x334(%eax), %eax
  461116: 33 d2                        	xorl	%edx, %edx
  461118: e8 83 22 fd ff               	calll	0x4333a0 <CODE+0x323a0>
  46111d: 68 e4 12 46 00               	pushl	$0x4612e4               # imm = 0x4612E4
  461122: 8d 55 88                     	leal	-0x78(%ebp), %edx
  461125: a1 18 5c 46 00               	movl	0x465c18, %eax
  46112a: e8 a1 6c fa ff               	calll	0x407dd0 <CODE+0x6dd0>
  46112f: ff 75 88                     	pushl	-0x78(%ebp)
  461132: 68 f0 12 46 00               	pushl	$0x4612f0               # imm = 0x4612F0
  461137: 8d 55 84                     	leal	-0x7c(%ebp), %edx
  46113a: a1 18 5c 46 00               	movl	0x465c18, %eax
  46113f: e8 8c 6c fa ff               	calll	0x407dd0 <CODE+0x6dd0>
  461144: ff 75 84                     	pushl	-0x7c(%ebp)
  461147: 68 fc 12 46 00               	pushl	$0x4612fc               # imm = 0x4612FC
  46114c: 8d 45 8c                     	leal	-0x74(%ebp), %eax
  46114f: ba 05 00 00 00               	movl	$0x5, %edx
  461154: e8 db 30 fa ff               	calll	0x404234 <CODE+0x3234>
  461159: 8b 45 8c                     	movl	-0x74(%ebp), %eax
  46115c: 50                           	pushl	%eax
  46115d: 8b 45 fc                     	movl	-0x4(%ebp), %eax
  461160: 8b 80 28 03 00 00            	movl	0x328(%eax), %eax
  461166: 33 c9                        	xorl	%ecx, %ecx
  461168: 33 d2                        	xorl	%edx, %edx
  46116a: e8 75 eb ff ff               	calll	0x45fce4 <CODE+0x5ece4>
  46116f: 68 a0 12 46 00               	pushl	$0x4612a0               # imm = 0x4612A0
  461174: 8d 95 7c ff ff ff            	leal	-0x84(%ebp), %edx
  46117a: a1 18 5c 46 00               	movl	0x465c18, %eax
  46117f: e8 4c 6c fa ff               	calll	0x407dd0 <CODE+0x6dd0>
  461184: ff b5 7c ff ff ff            	pushl	-0x84(%ebp)
  46118a: 68 ac 12 46 00               	pushl	$0x4612ac               # imm = 0x4612AC
  46118f: 8d 45 80                     	leal	-0x80(%ebp), %eax
  461192: ba 03 00 00 00               	movl	$0x3, %edx
  461197: e8 98 30 fa ff               	calll	0x404234 <CODE+0x3234>
  46119c: 8b 45 80                     	movl	-0x80(%ebp), %eax
  46119f: 50                           	pushl	%eax
  4611a0: 8b 45 fc                     	movl	-0x4(%ebp), %eax
  4611a3: 8b 80 28 03 00 00            	movl	0x328(%eax), %eax
  4611a9: 33 c9                        	xorl	%ecx, %ecx
  4611ab: ba 01 00 00 00               	movl	$0x1, %edx
  4611b0: e8 2f eb ff ff               	calll	0x45fce4 <CODE+0x5ece4>
  4611b5: eb 10                        	jmp	0x4611c7 <CODE+0x601c7>
  4611b7: ff 05 40 5c 46 00            	incl	0x465c40
  4611bd: b8 14 13 46 00               	movl	$0x461314, %eax         # imm = 0x461314
  4611c2: e8 65 65 fc ff               	calll	0x42772c <CODE+0x2672c>
  4611c7: 33 c0                        	xorl	%eax, %eax
  4611c9: 5a                           	popl	%edx
  4611ca: 59                           	popl	%ecx
  4611cb: 59                           	popl	%ecx
  4611cc: 64 89 10                     	movl	%edx, %fs:(%eax)
  4611cf: 68 0c 12 46 00               	pushl	$0x46120c               # imm = 0x46120C
  4611d4: 8d 85 7c ff ff ff            	leal	-0x84(%ebp), %eax
  4611da: ba 15 00 00 00               	movl	$0x15, %edx
  4611df: e8 f4 2c fa ff               	calll	0x403ed8 <CODE+0x2ed8>
  4611e4: 8d 45 d8                     	leal	-0x28(%ebp), %eax
  4611e7: ba 02 00 00 00               	movl	$0x2, %edx
  4611ec: e8 e7 2c fa ff               	calll	0x403ed8 <CODE+0x2ed8>
  4611f1: 8d 45 f4                     	leal	-0xc(%ebp), %eax
  4611f4: 8b 15 c4 09 46 00            	movl	0x4609c4, %edx
  4611fa: b9 02 00 00 00               	movl	$0x2, %ecx
  4611ff: e8 64 37 fa ff               	calll	0x404968 <CODE+0x3968>
  461204: c3                           	retl
  461205: e9 ae 26 fa ff               	jmp	0x4038b8 <CODE+0x28b8>
  46120a: eb c8                        	jmp	0x4611d4 <CODE+0x601d4>
  46120c: 5f                           	popl	%edi
  46120d: 5e                           	popl	%esi
  46120e: 5b                           	popl	%ebx
  46120f: 8b e5                        	movl	%ebp, %esp
  461211: 5d                           	popl	%ebp
  461212: c3                           	retl
  461213: 00 ff                        	addb	%bh, %bh
