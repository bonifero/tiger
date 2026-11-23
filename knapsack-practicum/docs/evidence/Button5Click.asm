
/Users/cassidal/Documents/vuz/tiger/source/Лаб_3/Загрузка_рюкзака.exe:	file format coff-i386

Disassembly of section CODE:

00401000 <CODE>:
  461abc: 55                           	pushl	%ebp
  461abd: 8b ec                        	movl	%esp, %ebp
  461abf: b9 08 00 00 00               	movl	$0x8, %ecx
  461ac4: 6a 00                        	pushl	$0x0
  461ac6: 6a 00                        	pushl	$0x0
  461ac8: 49                           	decl	%ecx
  461ac9: 75 f9                        	jne	0x461ac4 <CODE+0x60ac4>
  461acb: 53                           	pushl	%ebx
  461acc: 56                           	pushl	%esi
  461acd: 57                           	pushl	%edi
  461ace: 89 45 fc                     	movl	%eax, -0x4(%ebp)
  461ad1: 33 c0                        	xorl	%eax, %eax
  461ad3: 55                           	pushl	%ebp
  461ad4: 68 d7 1e 46 00               	pushl	$0x461ed7               # imm = 0x461ED7
  461ad9: 64 ff 30                     	pushl	%fs:(%eax)
  461adc: 64 89 20                     	movl	%esp, %fs:(%eax)
  461adf: c6 45 f7 01                  	movb	$0x1, -0x9(%ebp)
  461ae3: 6a 02                        	pushl	$0x2
  461ae5: b8 34 5c 46 00               	movl	$0x465c34, %eax         # imm = 0x465C34
  461aea: b9 01 00 00 00               	movl	$0x1, %ecx
  461aef: 8b 15 68 02 46 00            	movl	0x460268, %edx
  461af5: e8 9a 33 fa ff               	calll	0x404e94 <CODE+0x3e94>
  461afa: 83 c4 04                     	addl	$0x4, %esp
  461afd: 6a 02                        	pushl	$0x2
  461aff: 8d 45 f8                     	leal	-0x8(%ebp), %eax
  461b02: b9 01 00 00 00               	movl	$0x1, %ecx
  461b07: 8b 15 9c 1a 46 00            	movl	0x461a9c, %edx
  461b0d: e8 82 33 fa ff               	calll	0x404e94 <CODE+0x3e94>
  461b12: 83 c4 04                     	addl	$0x4, %esp
  461b15: a1 0c 5c 46 00               	movl	0x465c0c, %eax
  461b1a: 50                           	pushl	%eax
  461b1b: a1 34 5c 46 00               	movl	0x465c34, %eax
  461b20: b9 01 00 00 00               	movl	$0x1, %ecx
  461b25: 8b 15 48 02 46 00            	movl	0x460248, %edx
  461b2b: e8 64 33 fa ff               	calll	0x404e94 <CODE+0x3e94>
  461b30: 83 c4 04                     	addl	$0x4, %esp
  461b33: a1 0c 5c 46 00               	movl	0x465c0c, %eax
  461b38: 50                           	pushl	%eax
  461b39: 8b 45 f8                     	movl	-0x8(%ebp), %eax
  461b3c: b9 01 00 00 00               	movl	$0x1, %ecx
  461b41: 8b 15 7c 1a 46 00            	movl	0x461a7c, %edx
  461b47: e8 48 33 fa ff               	calll	0x404e94 <CODE+0x3e94>
  461b4c: 83 c4 04                     	addl	$0x4, %esp
  461b4f: a1 0c 5c 46 00               	movl	0x465c0c, %eax
  461b54: 50                           	pushl	%eax
  461b55: a1 34 5c 46 00               	movl	0x465c34, %eax
  461b5a: 83 c0 04                     	addl	$0x4, %eax
  461b5d: b9 01 00 00 00               	movl	$0x1, %ecx
  461b62: 8b 15 48 02 46 00            	movl	0x460248, %edx
  461b68: e8 27 33 fa ff               	calll	0x404e94 <CODE+0x3e94>
  461b6d: 83 c4 04                     	addl	$0x4, %esp
  461b70: a1 0c 5c 46 00               	movl	0x465c0c, %eax
  461b75: 50                           	pushl	%eax
  461b76: 8b 45 f8                     	movl	-0x8(%ebp), %eax
  461b79: 83 c0 04                     	addl	$0x4, %eax
  461b7c: b9 01 00 00 00               	movl	$0x1, %ecx
  461b81: 8b 15 7c 1a 46 00            	movl	0x461a7c, %edx
  461b87: e8 08 33 fa ff               	calll	0x404e94 <CODE+0x3e94>
  461b8c: 83 c4 04                     	addl	$0x4, %esp
  461b8f: 8b 3d 0c 5c 46 00            	movl	0x465c0c, %edi
  461b95: 85 ff                        	testl	%edi, %edi
  461b97: 0f 8e 8f 00 00 00            	jle	0x461c2c <CODE+0x60c2c>
  461b9d: bb 01 00 00 00               	movl	$0x1, %ebx
  461ba2: 83 fb 01                     	cmpl	$0x1, %ebx
  461ba5: 75 0d                        	jne	0x461bb4 <CODE+0x60bb4>
  461ba7: a1 34 5c 46 00               	movl	0x465c34, %eax
  461bac: 8b 00                        	movl	(%eax), %eax
  461bae: 33 d2                        	xorl	%edx, %edx
  461bb0: 89 10                        	movl	%edx, (%eax)
  461bb2: eb 44                        	jmp	0x461bf8 <CODE+0x60bf8>
  461bb4: 8d 45 f0                     	leal	-0x10(%ebp), %eax
  461bb7: 50                           	pushl	%eax
  461bb8: 8b cb                        	movl	%ebx, %ecx
  461bba: 49                           	decl	%ecx
  461bbb: 8b 45 fc                     	movl	-0x4(%ebp), %eax
  461bbe: 8b 80 fc 02 00 00            	movl	0x2fc(%eax), %eax
  461bc4: 33 d2                        	xorl	%edx, %edx
  461bc6: e8 a9 e0 ff ff               	calll	0x45fc74 <CODE+0x5ec74>
  461bcb: 8b 45 f0                     	movl	-0x10(%ebp), %eax
  461bce: e8 39 63 fa ff               	calll	0x407f0c <CODE+0x6f0c>
  461bd3: 8b 15 34 5c 46 00            	movl	0x465c34, %edx
  461bd9: 8b 52 04                     	movl	0x4(%edx), %edx
  461bdc: f7 6c 9a f8                  	imull	-0x8(%edx,%ebx,4)
  461be0: 8b 15 34 5c 46 00            	movl	0x465c34, %edx
  461be6: 8b 12                        	movl	(%edx), %edx
  461be8: 03 44 9a f8                  	addl	-0x8(%edx,%ebx,4), %eax
  461bec: 8b 15 34 5c 46 00            	movl	0x465c34, %edx
  461bf2: 8b 12                        	movl	(%edx), %edx
  461bf4: 89 44 9a fc                  	movl	%eax, -0x4(%edx,%ebx,4)
  461bf8: a1 0c 5c 46 00               	movl	0x465c0c, %eax
  461bfd: 2b c3                        	subl	%ebx, %eax
  461bff: 8b 15 30 5c 46 00            	movl	0x465c30, %edx
  461c05: 8b 04 82                     	movl	(%edx,%eax,4), %eax
  461c08: 8b 15 34 5c 46 00            	movl	0x465c34, %edx
  461c0e: 8b 12                        	movl	(%edx), %edx
  461c10: 8b 54 9a fc                  	movl	-0x4(%edx,%ebx,4), %edx
  461c14: 8b 04 90                     	movl	(%eax,%edx,4), %eax
  461c17: 8b 15 34 5c 46 00            	movl	0x465c34, %edx
  461c1d: 8b 52 04                     	movl	0x4(%edx), %edx
  461c20: 89 44 9a fc                  	movl	%eax, -0x4(%edx,%ebx,4)
  461c24: 43                           	incl	%ebx
  461c25: 4f                           	decl	%edi
  461c26: 0f 85 76 ff ff ff            	jne	0x461ba2 <CODE+0x60ba2>
  461c2c: 8d 45 ec                     	leal	-0x14(%ebp), %eax
  461c2f: 50                           	pushl	%eax
  461c30: 8b 45 fc                     	movl	-0x4(%ebp), %eax
  461c33: 8b 80 fc 02 00 00            	movl	0x2fc(%eax), %eax
  461c39: 8b 0d 0c 5c 46 00            	movl	0x465c0c, %ecx
  461c3f: 33 d2                        	xorl	%edx, %edx
  461c41: e8 2e e0 ff ff               	calll	0x45fc74 <CODE+0x5ec74>
  461c46: 8b 45 ec                     	movl	-0x14(%ebp), %eax
  461c49: e8 be 62 fa ff               	calll	0x407f0c <CODE+0x6f0c>
  461c4e: 8b 15 34 5c 46 00            	movl	0x465c34, %edx
  461c54: 8b 52 04                     	movl	0x4(%edx), %edx
  461c57: 8b 0d 0c 5c 46 00            	movl	0x465c0c, %ecx
  461c5d: f7 6c 8a fc                  	imull	-0x4(%edx,%ecx,4)
  461c61: 8b 15 34 5c 46 00            	movl	0x465c34, %edx
  461c67: 8b 12                        	movl	(%edx), %edx
  461c69: 8b 0d 0c 5c 46 00            	movl	0x465c0c, %ecx
  461c6f: 03 44 8a fc                  	addl	-0x4(%edx,%ecx,4), %eax
  461c73: a3 38 5c 46 00               	movl	%eax, 0x465c38
  461c78: a1 2c 5c 46 00               	movl	0x465c2c, %eax
  461c7d: 8b 15 0c 5c 46 00            	movl	0x465c0c, %edx
  461c83: 8b 44 90 fc                  	movl	-0x4(%eax,%edx,4), %eax
  461c87: 8b 00                        	movl	(%eax), %eax
  461c89: a3 3c 5c 46 00               	movl	%eax, 0x465c3c
  461c8e: 33 db                        	xorl	%ebx, %ebx
  461c90: 8b 3d 0c 5c 46 00            	movl	0x465c0c, %edi
  461c96: 4f                           	decl	%edi
  461c97: 85 ff                        	testl	%edi, %edi
  461c99: 7c 54                        	jl	0x461cef <CODE+0x60cef>
  461c9b: 47                           	incl	%edi
  461c9c: 33 f6                        	xorl	%esi, %esi
  461c9e: 8d 45 e8                     	leal	-0x18(%ebp), %eax
  461ca1: 50                           	pushl	%eax
  461ca2: 8d 4e 01                     	leal	0x1(%esi), %ecx
  461ca5: 8d 53 01                     	leal	0x1(%ebx), %edx
  461ca8: 8b 45 fc                     	movl	-0x4(%ebp), %eax
  461cab: 8b 80 2c 03 00 00            	movl	0x32c(%eax), %eax
  461cb1: e8 be df ff ff               	calll	0x45fc74 <CODE+0x5ec74>
  461cb6: 83 7d e8 00                  	cmpl	$0x0, -0x18(%ebp)
  461cba: 75 06                        	jne	0x461cc2 <CODE+0x60cc2>
  461cbc: c6 45 f7 00                  	movb	$0x0, -0x9(%ebp)
  461cc0: eb 29                        	jmp	0x461ceb <CODE+0x60ceb>
  461cc2: 8d 45 e4                     	leal	-0x1c(%ebp), %eax
  461cc5: 50                           	pushl	%eax
  461cc6: 8d 4e 01                     	leal	0x1(%esi), %ecx
  461cc9: 8d 53 01                     	leal	0x1(%ebx), %edx
  461ccc: 8b 45 fc                     	movl	-0x4(%ebp), %eax
  461ccf: 8b 80 2c 03 00 00            	movl	0x32c(%eax), %eax
  461cd5: e8 9a df ff ff               	calll	0x45fc74 <CODE+0x5ec74>
  461cda: 8b 45 e4                     	movl	-0x1c(%ebp), %eax
  461cdd: e8 2a 62 fa ff               	calll	0x407f0c <CODE+0x6f0c>
  461ce2: 8b 55 f8                     	movl	-0x8(%ebp), %edx
  461ce5: 8b 14 9a                     	movl	(%edx,%ebx,4), %edx
  461ce8: 89 04 b2                     	movl	%eax, (%edx,%esi,4)
  461ceb: 46                           	incl	%esi
  461cec: 4f                           	decl	%edi
  461ced: 75 af                        	jne	0x461c9e <CODE+0x60c9e>
  461cef: 43                           	incl	%ebx
  461cf0: 83 fb 02                     	cmpl	$0x2, %ebx
  461cf3: 75 9b                        	jne	0x461c90 <CODE+0x60c90>
  461cf5: 33 db                        	xorl	%ebx, %ebx
  461cf7: 8b 3d 0c 5c 46 00            	movl	0x465c0c, %edi
  461cfd: 4f                           	decl	%edi
  461cfe: 85 ff                        	testl	%edi, %edi
  461d00: 7c 22                        	jl	0x461d24 <CODE+0x60d24>
  461d02: 47                           	incl	%edi
  461d03: 33 f6                        	xorl	%esi, %esi
  461d05: 8b 45 f8                     	movl	-0x8(%ebp), %eax
  461d08: 8b 04 98                     	movl	(%eax,%ebx,4), %eax
  461d0b: 8b 04 b0                     	movl	(%eax,%esi,4), %eax
  461d0e: 8b 15 34 5c 46 00            	movl	0x465c34, %edx
  461d14: 8b 14 9a                     	movl	(%edx,%ebx,4), %edx
  461d17: 3b 04 b2                     	cmpl	(%edx,%esi,4), %eax
  461d1a: 74 04                        	je	0x461d20 <CODE+0x60d20>
  461d1c: c6 45 f7 00                  	movb	$0x0, -0x9(%ebp)
  461d20: 46                           	incl	%esi
  461d21: 4f                           	decl	%edi
  461d22: 75 e1                        	jne	0x461d05 <CODE+0x60d05>
  461d24: 43                           	incl	%ebx
  461d25: 83 fb 02                     	cmpl	$0x2, %ebx
  461d28: 75 cd                        	jne	0x461cf7 <CODE+0x60cf7>
  461d2a: 80 7d f7 00                  	cmpb	$0x0, -0x9(%ebp)
  461d2e: 0f 84 6a 01 00 00            	je	0x461e9e <CODE+0x60e9e>
  461d34: b8 f0 1e 46 00               	movl	$0x461ef0, %eax         # imm = 0x461EF0
  461d39: e8 ee 59 fc ff               	calll	0x42772c <CODE+0x2672c>
  461d3e: 8b 45 fc                     	movl	-0x4(%ebp), %eax
  461d41: 8b 80 4c 03 00 00            	movl	0x34c(%eax), %eax
  461d47: b2 01                        	movb	$0x1, %dl
  461d49: e8 52 16 fd ff               	calll	0x4333a0 <CODE+0x323a0>
  461d4e: 83 3d 40 5c 46 00 01         	cmpl	$0x1, 0x465c40
  461d55: 75 3d                        	jne	0x461d94 <CODE+0x60d94>
  461d57: 68 14 1f 46 00               	pushl	$0x461f14               # imm = 0x461F14
  461d5c: 8d 55 dc                     	leal	-0x24(%ebp), %edx
  461d5f: a1 40 5c 46 00               	movl	0x465c40, %eax
  461d64: e8 67 60 fa ff               	calll	0x407dd0 <CODE+0x6dd0>
  461d69: ff 75 dc                     	pushl	-0x24(%ebp)
  461d6c: 68 34 1f 46 00               	pushl	$0x461f34               # imm = 0x461F34
  461d71: 8d 45 e0                     	leal	-0x20(%ebp), %eax
  461d74: ba 03 00 00 00               	movl	$0x3, %edx
  461d79: e8 b6 24 fa ff               	calll	0x404234 <CODE+0x3234>
  461d7e: 8b 55 e0                     	movl	-0x20(%ebp), %edx
  461d81: 8b 45 fc                     	movl	-0x4(%ebp), %eax
  461d84: 8b 80 4c 03 00 00            	movl	0x34c(%eax), %eax
  461d8a: e8 21 17 fd ff               	calll	0x4334b0 <CODE+0x324b0>
  461d8f: e9 96 00 00 00               	jmp	0x461e2a <CODE+0x60e2a>
  461d94: 83 3d 40 5c 46 00 00         	cmpl	$0x0, 0x465c40
  461d9b: 74 09                        	je	0x461da6 <CODE+0x60da6>
  461d9d: 83 3d 40 5c 46 00 04         	cmpl	$0x4, 0x465c40
  461da4: 7e 3a                        	jle	0x461de0 <CODE+0x60de0>
  461da6: 68 48 1f 46 00               	pushl	$0x461f48               # imm = 0x461F48
  461dab: 8d 55 d4                     	leal	-0x2c(%ebp), %edx
  461dae: a1 40 5c 46 00               	movl	0x465c40, %eax
  461db3: e8 18 60 fa ff               	calll	0x407dd0 <CODE+0x6dd0>
  461db8: ff 75 d4                     	pushl	-0x2c(%ebp)
  461dbb: 68 68 1f 46 00               	pushl	$0x461f68               # imm = 0x461F68
  461dc0: 8d 45 d8                     	leal	-0x28(%ebp), %eax
  461dc3: ba 03 00 00 00               	movl	$0x3, %edx
  461dc8: e8 67 24 fa ff               	calll	0x404234 <CODE+0x3234>
  461dcd: 8b 55 d8                     	movl	-0x28(%ebp), %edx
  461dd0: 8b 45 fc                     	movl	-0x4(%ebp), %eax
  461dd3: 8b 80 4c 03 00 00            	movl	0x34c(%eax), %eax
  461dd9: e8 d2 16 fd ff               	calll	0x4334b0 <CODE+0x324b0>
  461dde: eb 4a                        	jmp	0x461e2a <CODE+0x60e2a>
  461de0: 83 3d 40 5c 46 00 02         	cmpl	$0x2, 0x465c40
  461de7: 74 09                        	je	0x461df2 <CODE+0x60df2>
  461de9: 83 3d 40 5c 46 00 03         	cmpl	$0x3, 0x465c40
  461df0: 75 38                        	jne	0x461e2a <CODE+0x60e2a>
  461df2: 68 48 1f 46 00               	pushl	$0x461f48               # imm = 0x461F48
  461df7: 8d 55 cc                     	leal	-0x34(%ebp), %edx
  461dfa: a1 40 5c 46 00               	movl	0x465c40, %eax
  461dff: e8 cc 5f fa ff               	calll	0x407dd0 <CODE+0x6dd0>
  461e04: ff 75 cc                     	pushl	-0x34(%ebp)
  461e07: 68 7c 1f 46 00               	pushl	$0x461f7c               # imm = 0x461F7C
  461e0c: 8d 45 d0                     	leal	-0x30(%ebp), %eax
  461e0f: ba 03 00 00 00               	movl	$0x3, %edx
  461e14: e8 1b 24 fa ff               	calll	0x404234 <CODE+0x3234>
  461e19: 8b 55 d0                     	movl	-0x30(%ebp), %edx
  461e1c: 8b 45 fc                     	movl	-0x4(%ebp), %eax
  461e1f: 8b 80 4c 03 00 00            	movl	0x34c(%eax), %eax
  461e25: e8 86 16 fd ff               	calll	0x4334b0 <CODE+0x324b0>
  461e2a: 8b 45 fc                     	movl	-0x4(%ebp), %eax
  461e2d: 8b 80 00 03 00 00            	movl	0x300(%eax), %eax
  461e33: b2 01                        	movb	$0x1, %dl
  461e35: e8 66 15 fd ff               	calll	0x4333a0 <CODE+0x323a0>
  461e3a: 68 90 1f 46 00               	pushl	$0x461f90               # imm = 0x461F90
  461e3f: 8d 55 c4                     	leal	-0x3c(%ebp), %edx
  461e42: a1 38 5c 46 00               	movl	0x465c38, %eax
  461e47: e8 84 5f fa ff               	calll	0x407dd0 <CODE+0x6dd0>
  461e4c: ff 75 c4                     	pushl	-0x3c(%ebp)
  461e4f: 68 b0 1f 46 00               	pushl	$0x461fb0               # imm = 0x461FB0
  461e54: 68 bc 1f 46 00               	pushl	$0x461fbc               # imm = 0x461FBC
  461e59: 68 c8 1f 46 00               	pushl	$0x461fc8               # imm = 0x461FC8
  461e5e: 8d 55 c0                     	leal	-0x40(%ebp), %edx
  461e61: a1 3c 5c 46 00               	movl	0x465c3c, %eax
  461e66: e8 65 5f fa ff               	calll	0x407dd0 <CODE+0x6dd0>
  461e6b: ff 75 c0                     	pushl	-0x40(%ebp)
  461e6e: 8d 45 c8                     	leal	-0x38(%ebp), %eax
  461e71: ba 06 00 00 00               	movl	$0x6, %edx
  461e76: e8 b9 23 fa ff               	calll	0x404234 <CODE+0x3234>
  461e7b: 8b 55 c8                     	movl	-0x38(%ebp), %edx
  461e7e: 8b 45 fc                     	movl	-0x4(%ebp), %eax
  461e81: 8b 80 14 03 00 00            	movl	0x314(%eax), %eax
  461e87: e8 24 16 fd ff               	calll	0x4334b0 <CODE+0x324b0>
  461e8c: 8b 45 fc                     	movl	-0x4(%ebp), %eax
  461e8f: 8b 80 3c 03 00 00            	movl	0x33c(%eax), %eax
  461e95: 33 d2                        	xorl	%edx, %edx
  461e97: e8 04 15 fd ff               	calll	0x4333a0 <CODE+0x323a0>
  461e9c: eb 10                        	jmp	0x461eae <CODE+0x60eae>
  461e9e: ff 05 40 5c 46 00            	incl	0x465c40
  461ea4: b8 dc 1f 46 00               	movl	$0x461fdc, %eax         # imm = 0x461FDC
  461ea9: e8 7e 58 fc ff               	calll	0x42772c <CODE+0x2672c>
  461eae: 33 c0                        	xorl	%eax, %eax
  461eb0: 5a                           	popl	%edx
  461eb1: 59                           	popl	%ecx
  461eb2: 59                           	popl	%ecx
  461eb3: 64 89 10                     	movl	%edx, %fs:(%eax)
  461eb6: 68 de 1e 46 00               	pushl	$0x461ede               # imm = 0x461EDE
  461ebb: 8d 45 c0                     	leal	-0x40(%ebp), %eax
  461ebe: ba 0d 00 00 00               	movl	$0xd, %edx
  461ec3: e8 10 20 fa ff               	calll	0x403ed8 <CODE+0x2ed8>
  461ec8: 8d 45 f8                     	leal	-0x8(%ebp), %eax
  461ecb: 8b 15 9c 1a 46 00            	movl	0x461a9c, %edx
  461ed1: e8 ca 2f fa ff               	calll	0x404ea0 <CODE+0x3ea0>
  461ed6: c3                           	retl
  461ed7: e9 dc 19 fa ff               	jmp	0x4038b8 <CODE+0x28b8>
  461edc: eb dd                        	jmp	0x461ebb <CODE+0x60ebb>
  461ede: 5f                           	popl	%edi
  461edf: 5e                           	popl	%esi
  461ee0: 5b                           	popl	%ebx
  461ee1: 8b e5                        	movl	%ebp, %esp
  461ee3: 5d                           	popl	%ebp
  461ee4: c3                           	retl
  461ee5: 00 00                        	addb	%al, (%eax)
  461ee7: 00 ff                        	addb	%bh, %bh
  461ee9: ff ff                        	<unknown>
  461eeb: ff 1a                        	lcalll	*(%edx)
  461eed: 00 00                        	addb	%al, (%eax)
  461eef: 00 cf                        	addb	%cl, %bh
  461ef1: ee                           	outb	%al, %dx
  461ef2: e7 e4                        	outl	%eax, $0xe4
  461ef4: f0                           	lock
  461ef5: e0 e2                        	loopne	0x461ed9 <CODE+0x60ed9>
  461ef7: eb ff                        	jmp	0x461ef8 <CODE+0x60ef8>
  461ef9: fe 2e                        	<unknown>
  461efb: 20 c7                        	andb	%al, %bh
  461efd: e0 e4                        	loopne	0x461ee3 <CODE+0x60ee3>
  461eff: e0 f7                        	loopne	0x461ef8 <CODE+0x60ef8>
