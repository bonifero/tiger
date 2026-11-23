
/Users/cassidal/Documents/vuz/tiger/source/Лаб_3/Загрузка_рюкзака.exe:	file format coff-i386

Disassembly of section CODE:

00401000 <CODE>:
  46064c: 55                           	pushl	%ebp
  46064d: 8b ec                        	movl	%esp, %ebp
  46064f: b9 06 00 00 00               	movl	$0x6, %ecx
  460654: 6a 00                        	pushl	$0x0
  460656: 6a 00                        	pushl	$0x0
  460658: 49                           	decl	%ecx
  460659: 75 f9                        	jne	0x460654 <CODE+0x5f654>
  46065b: 53                           	pushl	%ebx
  46065c: 56                           	pushl	%esi
  46065d: 57                           	pushl	%edi
  46065e: 8b d8                        	movl	%eax, %ebx
  460660: 33 c0                        	xorl	%eax, %eax
  460662: 55                           	pushl	%ebp
  460663: 68 36 09 46 00               	pushl	$0x460936               # imm = 0x460936
  460668: 64 ff 30                     	pushl	%fs:(%eax)
  46066b: 64 89 20                     	movl	%esp, %fs:(%eax)
  46066e: b2 01                        	movb	$0x1, %dl
  460670: 8b 83 40 03 00 00            	movl	0x340(%ebx), %eax
  460676: e8 25 2d fd ff               	calll	0x4333a0 <CODE+0x323a0>
  46067b: 33 d2                        	xorl	%edx, %edx
  46067d: 8b 83 f8 02 00 00            	movl	0x2f8(%ebx), %eax
  460683: 8b 08                        	movl	(%eax), %ecx
  460685: ff 51 64                     	calll	*0x64(%ecx)
  460688: 33 d2                        	xorl	%edx, %edx
  46068a: 8b 83 fc 02 00 00            	movl	0x2fc(%ebx), %eax
  460690: 8b 08                        	movl	(%eax), %ecx
  460692: ff 51 64                     	calll	*0x64(%ecx)
  460695: b2 01                        	movb	$0x1, %dl
  460697: 8b 83 50 03 00 00            	movl	0x350(%ebx), %eax
  46069d: e8 fe 2c fd ff               	calll	0x4333a0 <CODE+0x323a0>
  4606a2: 83 3d 18 5c 46 00 00         	cmpl	$0x0, 0x465c18
  4606a9: 0f 8e 5f 02 00 00            	jle	0x46090e <CODE+0x5f90e>
  4606af: 8d 55 f0                     	leal	-0x10(%ebp), %edx
  4606b2: a1 10 5c 46 00               	movl	0x465c10, %eax
  4606b7: 2b 05 18 5c 46 00            	subl	0x465c18, %eax
  4606bd: 40                           	incl	%eax
  4606be: e8 0d 77 fa ff               	calll	0x407dd0 <CODE+0x6dd0>
  4606c3: 8b 4d f0                     	movl	-0x10(%ebp), %ecx
  4606c6: 8d 45 f4                     	leal	-0xc(%ebp), %eax
  4606c9: ba 4c 09 46 00               	movl	$0x46094c, %edx         # imm = 0x46094C
  4606ce: e8 ed 3a fa ff               	calll	0x4041c0 <CODE+0x31c0>
  4606d3: 8b 55 f4                     	movl	-0xc(%ebp), %edx
  4606d6: 8b 83 1c 03 00 00            	movl	0x31c(%ebx), %eax
  4606dc: e8 cf 2d fd ff               	calll	0x4334b0 <CODE+0x324b0>
  4606e1: 68 64 09 46 00               	pushl	$0x460964               # imm = 0x460964
  4606e6: 8d 55 e8                     	leal	-0x18(%ebp), %edx
  4606e9: a1 0c 5c 46 00               	movl	0x465c0c, %eax
  4606ee: 2b 05 18 5c 46 00            	subl	0x465c18, %eax
  4606f4: 40                           	incl	%eax
  4606f5: e8 d6 76 fa ff               	calll	0x407dd0 <CODE+0x6dd0>
  4606fa: ff 75 e8                     	pushl	-0x18(%ebp)
  4606fd: 68 74 09 46 00               	pushl	$0x460974               # imm = 0x460974
  460702: 8d 55 e4                     	leal	-0x1c(%ebp), %edx
  460705: a1 18 5c 46 00               	movl	0x465c18, %eax
  46070a: e8 c1 76 fa ff               	calll	0x407dd0 <CODE+0x6dd0>
  46070f: ff 75 e4                     	pushl	-0x1c(%ebp)
  460712: 68 84 09 46 00               	pushl	$0x460984               # imm = 0x460984
  460717: 8d 45 ec                     	leal	-0x14(%ebp), %eax
  46071a: ba 05 00 00 00               	movl	$0x5, %edx
  46071f: e8 10 3b fa ff               	calll	0x404234 <CODE+0x3234>
  460724: 8b 55 ec                     	movl	-0x14(%ebp), %edx
  460727: 8b 83 50 03 00 00            	movl	0x350(%ebx), %eax
  46072d: e8 7e 2d fd ff               	calll	0x4334b0 <CODE+0x324b0>
  460732: 8b 15 14 5c 46 00            	movl	0x465c14, %edx
  460738: 83 c2 02                     	addl	$0x2, %edx
  46073b: 8b 83 24 03 00 00            	movl	0x324(%ebx), %eax
  460741: e8 22 d4 ff ff               	calll	0x45db68 <CODE+0x5cb68>
  460746: 8d 45 e0                     	leal	-0x20(%ebp), %eax
  460749: 50                           	pushl	%eax
  46074a: 8b 0d 18 5c 46 00            	movl	0x465c18, %ecx
  460750: 33 d2                        	xorl	%edx, %edx
  460752: 8b 83 fc 02 00 00            	movl	0x2fc(%ebx), %eax
  460758: e8 17 f5 ff ff               	calll	0x45fc74 <CODE+0x5ec74>
  46075d: 8b 45 e0                     	movl	-0x20(%ebp), %eax
  460760: e8 a7 77 fa ff               	calll	0x407f0c <CODE+0x6f0c>
  460765: 89 45 dc                     	movl	%eax, -0x24(%ebp)
  460768: db 45 dc                     	fildl	-0x24(%ebp)
  46076b: db 05 14 5c 46 00            	fildl	0x465c14
  460771: de f1                        	fdivp	%st, %st(1)
  460773: e8 a4 21 fa ff               	calll	0x40291c <CODE+0x191c>
  460778: e8 bf 21 fa ff               	calll	0x40293c <CODE+0x193c>
  46077d: 8b d0                        	movl	%eax, %edx
  46077f: 83 c2 02                     	addl	$0x2, %edx
  460782: 8b 83 24 03 00 00            	movl	0x324(%ebx), %eax
  460788: e8 4b d0 ff ff               	calll	0x45d7d8 <CODE+0x5c7d8>
  46078d: 8d 45 d8                     	leal	-0x28(%ebp), %eax
  460790: 50                           	pushl	%eax
  460791: 8b 0d 18 5c 46 00            	movl	0x465c18, %ecx
  460797: 33 d2                        	xorl	%edx, %edx
  460799: 8b 83 fc 02 00 00            	movl	0x2fc(%ebx), %eax
  46079f: e8 d0 f4 ff ff               	calll	0x45fc74 <CODE+0x5ec74>
  4607a4: 8b 45 d8                     	movl	-0x28(%ebp), %eax
  4607a7: e8 60 77 fa ff               	calll	0x407f0c <CODE+0x6f0c>
  4607ac: 89 45 dc                     	movl	%eax, -0x24(%ebp)
  4607af: db 45 dc                     	fildl	-0x24(%ebp)
  4607b2: db 05 14 5c 46 00            	fildl	0x465c14
  4607b8: de f1                        	fdivp	%st, %st(1)
  4607ba: e8 5d 21 fa ff               	calll	0x40291c <CODE+0x191c>
  4607bf: e8 78 21 fa ff               	calll	0x40293c <CODE+0x193c>
  4607c4: 83 c0 02                     	addl	$0x2, %eax
  4607c7: 8b 15 0c 5c 46 00            	movl	0x465c0c, %edx
  4607cd: 2b 15 18 5c 46 00            	subl	0x465c18, %edx
  4607d3: 8b 0d 28 5c 46 00            	movl	0x465c28, %ecx
  4607d9: 89 04 91                     	movl	%eax, (%ecx,%edx,4)
  4607dc: 8b 15 14 5c 46 00            	movl	0x465c14, %edx
  4607e2: 83 c2 02                     	addl	$0x2, %edx
  4607e5: 8b 83 28 03 00 00            	movl	0x328(%ebx), %eax
  4607eb: e8 78 d3 ff ff               	calll	0x45db68 <CODE+0x5cb68>
  4607f0: 8b 83 24 03 00 00            	movl	0x324(%ebx), %eax
  4607f6: 8b 80 4c 02 00 00            	movl	0x24c(%eax), %eax
  4607fc: 85 c0                        	testl	%eax, %eax
  4607fe: 7e 3d                        	jle	0x46083d <CODE+0x5f83d>
  460800: 89 45 f8                     	movl	%eax, -0x8(%ebp)
  460803: c7 45 fc 01 00 00 00         	movl	$0x1, -0x4(%ebp)
  46080a: 8b 83 24 03 00 00            	movl	0x324(%ebx), %eax
  460810: 8b b8 1c 02 00 00            	movl	0x21c(%eax), %edi
  460816: 85 ff                        	testl	%edi, %edi
  460818: 7e 1b                        	jle	0x460835 <CODE+0x5f835>
  46081a: be 01 00 00 00               	movl	$0x1, %esi
  46081f: 6a 00                        	pushl	$0x0
  460821: 8b 4d fc                     	movl	-0x4(%ebp), %ecx
  460824: 8b d6                        	movl	%esi, %edx
  460826: 8b 83 24 03 00 00            	movl	0x324(%ebx), %eax
  46082c: e8 b3 f4 ff ff               	calll	0x45fce4 <CODE+0x5ece4>
  460831: 46                           	incl	%esi
  460832: 4f                           	decl	%edi
  460833: 75 ea                        	jne	0x46081f <CODE+0x5f81f>
  460835: ff 45 fc                     	incl	-0x4(%ebp)
  460838: ff 4d f8                     	decl	-0x8(%ebp)
  46083b: 75 cd                        	jne	0x46080a <CODE+0x5f80a>
  46083d: 8b 83 24 03 00 00            	movl	0x324(%ebx), %eax
  460843: 8b 80 4c 02 00 00            	movl	0x24c(%eax), %eax
  460849: 48                           	decl	%eax
  46084a: 85 c0                        	testl	%eax, %eax
  46084c: 7e 32                        	jle	0x460880 <CODE+0x5f880>
  46084e: 89 45 f8                     	movl	%eax, -0x8(%ebp)
  460851: c7 45 fc 01 00 00 00         	movl	$0x1, -0x4(%ebp)
  460858: 8d 55 d4                     	leal	-0x2c(%ebp), %edx
  46085b: 8b 45 fc                     	movl	-0x4(%ebp), %eax
  46085e: 48                           	decl	%eax
  46085f: e8 6c 75 fa ff               	calll	0x407dd0 <CODE+0x6dd0>
  460864: 8b 45 d4                     	movl	-0x2c(%ebp), %eax
  460867: 50                           	pushl	%eax
  460868: 8b 4d fc                     	movl	-0x4(%ebp), %ecx
  46086b: 33 d2                        	xorl	%edx, %edx
  46086d: 8b 83 24 03 00 00            	movl	0x324(%ebx), %eax
  460873: e8 6c f4 ff ff               	calll	0x45fce4 <CODE+0x5ece4>
  460878: ff 45 fc                     	incl	-0x4(%ebp)
  46087b: ff 4d f8                     	decl	-0x8(%ebp)
  46087e: 75 d8                        	jne	0x460858 <CODE+0x5f858>
  460880: 8b 83 24 03 00 00            	movl	0x324(%ebx), %eax
  460886: 8b 80 1c 02 00 00            	movl	0x21c(%eax), %eax
  46088c: 48                           	decl	%eax
  46088d: 85 c0                        	testl	%eax, %eax
  46088f: 7e 2c                        	jle	0x4608bd <CODE+0x5f8bd>
  460891: 89 45 f8                     	movl	%eax, -0x8(%ebp)
  460894: be 01 00 00 00               	movl	$0x1, %esi
  460899: 8d 55 d0                     	leal	-0x30(%ebp), %edx
  46089c: 8b c6                        	movl	%esi, %eax
  46089e: 48                           	decl	%eax
  46089f: e8 2c 75 fa ff               	calll	0x407dd0 <CODE+0x6dd0>
  4608a4: 8b 45 d0                     	movl	-0x30(%ebp), %eax
  4608a7: 50                           	pushl	%eax
  4608a8: 33 c9                        	xorl	%ecx, %ecx
  4608aa: 8b d6                        	movl	%esi, %edx
  4608ac: 8b 83 24 03 00 00            	movl	0x324(%ebx), %eax
  4608b2: e8 2d f4 ff ff               	calll	0x45fce4 <CODE+0x5ece4>
  4608b7: 46                           	incl	%esi
  4608b8: ff 4d f8                     	decl	-0x8(%ebp)
  4608bb: 75 dc                        	jne	0x460899 <CODE+0x5f899>
  4608bd: b2 01                        	movb	$0x1, %dl
  4608bf: 8b 83 14 03 00 00            	movl	0x314(%ebx), %eax
  4608c5: e8 d6 2a fd ff               	calll	0x4333a0 <CODE+0x323a0>
  4608ca: ba 90 09 46 00               	movl	$0x460990, %edx         # imm = 0x460990
  4608cf: 8b 83 14 03 00 00            	movl	0x314(%ebx), %eax
  4608d5: e8 d6 2b fd ff               	calll	0x4334b0 <CODE+0x324b0>
  4608da: 33 d2                        	xorl	%edx, %edx
  4608dc: 8b 83 48 03 00 00            	movl	0x348(%ebx), %eax
  4608e2: e8 b9 2a fd ff               	calll	0x4333a0 <CODE+0x323a0>
  4608e7: 33 d2                        	xorl	%edx, %edx
  4608e9: 8b 83 1c 03 00 00            	movl	0x31c(%ebx), %eax
  4608ef: e8 ac 2a fd ff               	calll	0x4333a0 <CODE+0x323a0>
  4608f4: b2 01                        	movb	$0x1, %dl
  4608f6: 8b 83 34 03 00 00            	movl	0x334(%ebx), %eax
  4608fc: e8 9f 2a fd ff               	calll	0x4333a0 <CODE+0x323a0>
  460901: b2 01                        	movb	$0x1, %dl
  460903: 8b 83 24 03 00 00            	movl	0x324(%ebx), %eax
  460909: e8 92 2a fd ff               	calll	0x4333a0 <CODE+0x323a0>
  46090e: 33 c0                        	xorl	%eax, %eax
  460910: 5a                           	popl	%edx
  460911: 59                           	popl	%ecx
  460912: 59                           	popl	%ecx
  460913: 64 89 10                     	movl	%edx, %fs:(%eax)
  460916: 68 3d 09 46 00               	pushl	$0x46093d               # imm = 0x46093D
  46091b: 8d 45 d0                     	leal	-0x30(%ebp), %eax
  46091e: ba 03 00 00 00               	movl	$0x3, %edx
  460923: e8 b0 35 fa ff               	calll	0x403ed8 <CODE+0x2ed8>
  460928: 8d 45 e0                     	leal	-0x20(%ebp), %eax
  46092b: ba 06 00 00 00               	movl	$0x6, %edx
  460930: e8 a3 35 fa ff               	calll	0x403ed8 <CODE+0x2ed8>
  460935: c3                           	retl
  460936: e9 7d 2f fa ff               	jmp	0x4038b8 <CODE+0x28b8>
