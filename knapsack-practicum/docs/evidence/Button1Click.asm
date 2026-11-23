
/Users/cassidal/Documents/vuz/tiger/source/Лаб_3/Загрузка_рюкзака.exe:	file format coff-i386

Disassembly of section CODE:

00401000 <CODE>:
  4602c4: 55                           	pushl	%ebp
  4602c5: 8b ec                        	movl	%esp, %ebp
  4602c7: b9 05 00 00 00               	movl	$0x5, %ecx
  4602cc: 6a 00                        	pushl	$0x0
  4602ce: 6a 00                        	pushl	$0x0
  4602d0: 49                           	decl	%ecx
  4602d1: 75 f9                        	jne	0x4602cc <CODE+0x5f2cc>
  4602d3: 53                           	pushl	%ebx
  4602d4: 56                           	pushl	%esi
  4602d5: 57                           	pushl	%edi
  4602d6: 8b f0                        	movl	%eax, %esi
  4602d8: 33 c0                        	xorl	%eax, %eax
  4602da: 55                           	pushl	%ebp
  4602db: 68 b5 05 46 00               	pushl	$0x4605b5               # imm = 0x4605B5
  4602e0: 64 ff 30                     	pushl	%fs:(%eax)
  4602e3: 64 89 20                     	movl	%esp, %fs:(%eax)
  4602e6: c6 45 f7 01                  	movb	$0x1, -0x9(%ebp)
  4602ea: 8d 55 ec                     	leal	-0x14(%ebp), %edx
  4602ed: 8b 86 08 03 00 00            	movl	0x308(%esi), %eax
  4602f3: e8 88 31 fd ff               	calll	0x433480 <CODE+0x32480>
  4602f8: 83 7d ec 00                  	cmpl	$0x0, -0x14(%ebp)
  4602fc: 75 04                        	jne	0x460302 <CODE+0x5f302>
  4602fe: c6 45 f7 00                  	movb	$0x0, -0x9(%ebp)
  460302: a1 0c 5c 46 00               	movl	0x465c0c, %eax
  460307: 85 c0                        	testl	%eax, %eax
  460309: 7e 2b                        	jle	0x460336 <CODE+0x5f336>
  46030b: 89 45 f0                     	movl	%eax, -0x10(%ebp)
  46030e: bb 01 00 00 00               	movl	$0x1, %ebx
  460313: 8d 45 e8                     	leal	-0x18(%ebp), %eax
  460316: 50                           	pushl	%eax
  460317: 8b cb                        	movl	%ebx, %ecx
  460319: 33 d2                        	xorl	%edx, %edx
  46031b: 8b 86 fc 02 00 00            	movl	0x2fc(%esi), %eax
  460321: e8 4e f9 ff ff               	calll	0x45fc74 <CODE+0x5ec74>
  460326: 83 7d e8 00                  	cmpl	$0x0, -0x18(%ebp)
  46032a: 75 04                        	jne	0x460330 <CODE+0x5f330>
  46032c: c6 45 f7 00                  	movb	$0x0, -0x9(%ebp)
  460330: 43                           	incl	%ebx
  460331: ff 4d f0                     	decl	-0x10(%ebp)
  460334: 75 dd                        	jne	0x460313 <CODE+0x5f313>
  460336: a1 0c 5c 46 00               	movl	0x465c0c, %eax
  46033b: 48                           	decl	%eax
  46033c: 85 c0                        	testl	%eax, %eax
  46033e: 7c 44                        	jl	0x460384 <CODE+0x5f384>
  460340: 40                           	incl	%eax
  460341: 89 45 f0                     	movl	%eax, -0x10(%ebp)
  460344: c7 45 f8 00 00 00 00         	movl	$0x0, -0x8(%ebp)
  46034b: 8b 1d 0c 5c 46 00            	movl	0x465c0c, %ebx
  460351: 85 db                        	testl	%ebx, %ebx
  460353: 7c 27                        	jl	0x46037c <CODE+0x5f37c>
  460355: 43                           	incl	%ebx
  460356: 33 ff                        	xorl	%edi, %edi
  460358: 8d 45 e4                     	leal	-0x1c(%ebp), %eax
  46035b: 50                           	pushl	%eax
  46035c: 8b 4d f8                     	movl	-0x8(%ebp), %ecx
  46035f: 41                           	incl	%ecx
  460360: 8d 57 01                     	leal	0x1(%edi), %edx
  460363: 8b 86 f8 02 00 00            	movl	0x2f8(%esi), %eax
  460369: e8 06 f9 ff ff               	calll	0x45fc74 <CODE+0x5ec74>
  46036e: 83 7d e4 00                  	cmpl	$0x0, -0x1c(%ebp)
  460372: 75 04                        	jne	0x460378 <CODE+0x5f378>
  460374: c6 45 f7 00                  	movb	$0x0, -0x9(%ebp)
  460378: 47                           	incl	%edi
  460379: 4b                           	decl	%ebx
  46037a: 75 dc                        	jne	0x460358 <CODE+0x5f358>
  46037c: ff 45 f8                     	incl	-0x8(%ebp)
  46037f: ff 4d f0                     	decl	-0x10(%ebp)
  460382: 75 c7                        	jne	0x46034b <CODE+0x5f34b>
  460384: 80 7d f7 00                  	cmpb	$0x0, -0x9(%ebp)
  460388: 0f 84 df 01 00 00            	je	0x46056d <CODE+0x5f56d>
  46038e: 8d 55 e0                     	leal	-0x20(%ebp), %edx
  460391: 8b 86 08 03 00 00            	movl	0x308(%esi), %eax
  460397: e8 e4 30 fd ff               	calll	0x433480 <CODE+0x32480>
  46039c: 8b 45 e0                     	movl	-0x20(%ebp), %eax
  46039f: e8 68 7b fa ff               	calll	0x407f0c <CODE+0x6f0c>
  4603a4: a3 14 5c 46 00               	movl	%eax, 0x465c14
  4603a9: 83 3d 14 5c 46 00 02         	cmpl	$0x2, 0x465c14
  4603b0: 7d 04                        	jge	0x4603b6 <CODE+0x5f3b6>
  4603b2: c6 45 f7 00                  	movb	$0x0, -0x9(%ebp)
  4603b6: a1 0c 5c 46 00               	movl	0x465c0c, %eax
  4603bb: 50                           	pushl	%eax
  4603bc: b8 1c 5c 46 00               	movl	$0x465c1c, %eax         # imm = 0x465C1C
  4603c1: b9 01 00 00 00               	movl	$0x1, %ecx
  4603c6: 8b 15 28 01 46 00            	movl	0x460128, %edx
  4603cc: e8 c3 4a fa ff               	calll	0x404e94 <CODE+0x3e94>
  4603d1: 83 c4 04                     	addl	$0x4, %esp
  4603d4: a1 0c 5c 46 00               	movl	0x465c0c, %eax
  4603d9: 85 c0                        	testl	%eax, %eax
  4603db: 7e 3b                        	jle	0x460418 <CODE+0x5f418>
  4603dd: 89 45 f0                     	movl	%eax, -0x10(%ebp)
  4603e0: bf 01 00 00 00               	movl	$0x1, %edi
  4603e5: 8d 45 dc                     	leal	-0x24(%ebp), %eax
  4603e8: 50                           	pushl	%eax
  4603e9: 8b cf                        	movl	%edi, %ecx
  4603eb: 33 d2                        	xorl	%edx, %edx
  4603ed: 8b 86 fc 02 00 00            	movl	0x2fc(%esi), %eax
  4603f3: e8 7c f8 ff ff               	calll	0x45fc74 <CODE+0x5ec74>
  4603f8: 8b 45 dc                     	movl	-0x24(%ebp), %eax
  4603fb: e8 0c 7b fa ff               	calll	0x407f0c <CODE+0x6f0c>
  460400: 8b d8                        	movl	%eax, %ebx
  460402: a1 1c 5c 46 00               	movl	0x465c1c, %eax
  460407: 89 5c b8 fc                  	movl	%ebx, -0x4(%eax,%edi,4)
  46040b: 4b                           	decl	%ebx
  46040c: 7d 04                        	jge	0x460412 <CODE+0x5f412>
  46040e: c6 45 f7 00                  	movb	$0x0, -0x9(%ebp)
  460412: 47                           	incl	%edi
  460413: ff 4d f0                     	decl	-0x10(%ebp)
  460416: 75 cd                        	jne	0x4603e5 <CODE+0x5f3e5>
  460418: a1 0c 5c 46 00               	movl	0x465c0c, %eax
  46041d: 50                           	pushl	%eax
  46041e: b8 20 5c 46 00               	movl	$0x465c20, %eax         # imm = 0x465C20
  460423: b9 01 00 00 00               	movl	$0x1, %ecx
  460428: 8b 15 68 01 46 00            	movl	0x460168, %edx
  46042e: e8 61 4a fa ff               	calll	0x404e94 <CODE+0x3e94>
  460433: 83 c4 04                     	addl	$0x4, %esp
  460436: a1 0c 5c 46 00               	movl	0x465c0c, %eax
  46043b: 48                           	decl	%eax
  46043c: 85 c0                        	testl	%eax, %eax
  46043e: 7c 73                        	jl	0x4604b3 <CODE+0x5f4b3>
  460440: 40                           	incl	%eax
  460441: 89 45 f0                     	movl	%eax, -0x10(%ebp)
  460444: 33 ff                        	xorl	%edi, %edi
  460446: a1 0c 5c 46 00               	movl	0x465c0c, %eax
  46044b: 40                           	incl	%eax
  46044c: 50                           	pushl	%eax
  46044d: a1 20 5c 46 00               	movl	0x465c20, %eax
  460452: 8d 04 b8                     	leal	(%eax,%edi,4), %eax
  460455: b9 01 00 00 00               	movl	$0x1, %ecx
  46045a: 8b 15 48 01 46 00            	movl	0x460148, %edx
  460460: e8 2f 4a fa ff               	calll	0x404e94 <CODE+0x3e94>
  460465: 83 c4 04                     	addl	$0x4, %esp
  460468: 8b 1d 0c 5c 46 00            	movl	0x465c0c, %ebx
  46046e: 85 db                        	testl	%ebx, %ebx
  460470: 7c 3b                        	jl	0x4604ad <CODE+0x5f4ad>
  460472: 43                           	incl	%ebx
  460473: c7 45 fc 00 00 00 00         	movl	$0x0, -0x4(%ebp)
  46047a: 8d 45 d8                     	leal	-0x28(%ebp), %eax
  46047d: 50                           	pushl	%eax
  46047e: 8d 4f 01                     	leal	0x1(%edi), %ecx
  460481: 8b 55 fc                     	movl	-0x4(%ebp), %edx
  460484: 42                           	incl	%edx
  460485: 8b 86 f8 02 00 00            	movl	0x2f8(%esi), %eax
  46048b: e8 e4 f7 ff ff               	calll	0x45fc74 <CODE+0x5ec74>
  460490: 8b 45 d8                     	movl	-0x28(%ebp), %eax
  460493: e8 74 7a fa ff               	calll	0x407f0c <CODE+0x6f0c>
  460498: 8b 15 20 5c 46 00            	movl	0x465c20, %edx
  46049e: 8b 14 ba                     	movl	(%edx,%edi,4), %edx
  4604a1: 8b 4d fc                     	movl	-0x4(%ebp), %ecx
  4604a4: 89 04 8a                     	movl	%eax, (%edx,%ecx,4)
  4604a7: ff 45 fc                     	incl	-0x4(%ebp)
  4604aa: 4b                           	decl	%ebx
  4604ab: 75 cd                        	jne	0x46047a <CODE+0x5f47a>
  4604ad: 47                           	incl	%edi
  4604ae: ff 4d f0                     	decl	-0x10(%ebp)
  4604b1: 75 93                        	jne	0x460446 <CODE+0x5f446>
  4604b3: 80 7d f7 00                  	cmpb	$0x0, -0x9(%ebp)
  4604b7: 0f 84 9e 00 00 00            	je	0x46055b <CODE+0x5f55b>
  4604bd: 33 d2                        	xorl	%edx, %edx
  4604bf: 8b 86 18 03 00 00            	movl	0x318(%esi), %eax
  4604c5: e8 d6 2e fd ff               	calll	0x4333a0 <CODE+0x323a0>
  4604ca: b2 01                        	movb	$0x1, %dl
  4604cc: 8b 86 1c 03 00 00            	movl	0x31c(%esi), %eax
  4604d2: e8 c9 2e fd ff               	calll	0x4333a0 <CODE+0x323a0>
  4604d7: b8 cc 05 46 00               	movl	$0x4605cc, %eax         # imm = 0x4605CC
  4604dc: e8 4b 72 fc ff               	calll	0x42772c <CODE+0x2672c>
  4604e1: a1 0c 5c 46 00               	movl	0x465c0c, %eax
  4604e6: a3 18 5c 46 00               	movl	%eax, 0x465c18
  4604eb: a1 0c 5c 46 00               	movl	0x465c0c, %eax
  4604f0: 50                           	pushl	%eax
  4604f1: b8 2c 5c 46 00               	movl	$0x465c2c, %eax         # imm = 0x465C2C
  4604f6: b9 01 00 00 00               	movl	$0x1, %ecx
  4604fb: 8b 15 28 02 46 00            	movl	0x460228, %edx
  460501: e8 8e 49 fa ff               	calll	0x404e94 <CODE+0x3e94>
  460506: 83 c4 04                     	addl	$0x4, %esp
  460509: a1 0c 5c 46 00               	movl	0x465c0c, %eax
  46050e: 50                           	pushl	%eax
  46050f: b8 30 5c 46 00               	movl	$0x465c30, %eax         # imm = 0x465C30
  460514: b9 01 00 00 00               	movl	$0x1, %ecx
  460519: 8b 15 28 02 46 00            	movl	0x460228, %edx
  46051f: e8 70 49 fa ff               	calll	0x404e94 <CODE+0x3e94>
  460524: 83 c4 04                     	addl	$0x4, %esp
  460527: a1 0c 5c 46 00               	movl	0x465c0c, %eax
  46052c: 40                           	incl	%eax
  46052d: a3 10 5c 46 00               	movl	%eax, 0x465c10
  460532: 33 d2                        	xorl	%edx, %edx
  460534: 8b 86 f8 02 00 00            	movl	0x2f8(%esi), %eax
  46053a: 8b 08                        	movl	(%eax), %ecx
  46053c: ff 51 64                     	calll	*0x64(%ecx)
  46053f: 33 d2                        	xorl	%edx, %edx
  460541: 8b 86 fc 02 00 00            	movl	0x2fc(%esi), %eax
  460547: 8b 08                        	movl	(%eax), %ecx
  460549: ff 51 64                     	calll	*0x64(%ecx)
  46054c: 33 d2                        	xorl	%edx, %edx
  46054e: 8b 86 08 03 00 00            	movl	0x308(%esi), %eax
  460554: 8b 08                        	movl	(%eax), %ecx
  460556: ff 51 64                     	calll	*0x64(%ecx)
  460559: eb 22                        	jmp	0x46057d <CODE+0x5f57d>
  46055b: ff 05 40 5c 46 00            	incl	0x465c40
  460561: b8 ec 05 46 00               	movl	$0x4605ec, %eax         # imm = 0x4605EC
  460566: e8 c1 71 fc ff               	calll	0x42772c <CODE+0x2672c>
  46056b: eb 10                        	jmp	0x46057d <CODE+0x5f57d>
  46056d: ff 05 40 5c 46 00            	incl	0x465c40
  460573: b8 20 06 46 00               	movl	$0x460620, %eax         # imm = 0x460620
  460578: e8 af 71 fc ff               	calll	0x42772c <CODE+0x2672c>
  46057d: 33 c0                        	xorl	%eax, %eax
  46057f: 5a                           	popl	%edx
  460580: 59                           	popl	%ecx
  460581: 59                           	popl	%ecx
  460582: 64 89 10                     	movl	%edx, %fs:(%eax)
  460585: 68 bc 05 46 00               	pushl	$0x4605bc               # imm = 0x4605BC
  46058a: 8d 45 d8                     	leal	-0x28(%ebp), %eax
  46058d: ba 02 00 00 00               	movl	$0x2, %edx
  460592: e8 41 39 fa ff               	calll	0x403ed8 <CODE+0x2ed8>
  460597: 8d 45 e0                     	leal	-0x20(%ebp), %eax
  46059a: e8 15 39 fa ff               	calll	0x403eb4 <CODE+0x2eb4>
  46059f: 8d 45 e4                     	leal	-0x1c(%ebp), %eax
  4605a2: ba 02 00 00 00               	movl	$0x2, %edx
  4605a7: e8 2c 39 fa ff               	calll	0x403ed8 <CODE+0x2ed8>
  4605ac: 8d 45 ec                     	leal	-0x14(%ebp), %eax
  4605af: e8 00 39 fa ff               	calll	0x403eb4 <CODE+0x2eb4>
  4605b4: c3                           	retl
  4605b5: e9 fe 32 fa ff               	jmp	0x4038b8 <CODE+0x28b8>
  4605ba: eb ce                        	jmp	0x46058a <CODE+0x5f58a>
  4605bc: 5f                           	popl	%edi
  4605bd: 5e                           	popl	%esi
  4605be: 5b                           	popl	%ebx
  4605bf: 8b e5                        	movl	%ebp, %esp
  4605c1: 5d                           	popl	%ebp
  4605c2: c3                           	retl
