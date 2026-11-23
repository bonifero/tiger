
/Users/cassidal/Documents/vuz/tiger/source/Лаб_3/Загрузка_рюкзака.exe:	file format coff-i386

Disassembly of section CODE:

00401000 <CODE>:
  462004: 55                           	pushl	%ebp
  462005: 8b ec                        	movl	%esp, %ebp
  462007: 33 c9                        	xorl	%ecx, %ecx
  462009: 51                           	pushl	%ecx
  46200a: 51                           	pushl	%ecx
  46200b: 51                           	pushl	%ecx
  46200c: 51                           	pushl	%ecx
  46200d: 51                           	pushl	%ecx
  46200e: 51                           	pushl	%ecx
  46200f: 51                           	pushl	%ecx
  462010: 53                           	pushl	%ebx
  462011: 56                           	pushl	%esi
  462012: 57                           	pushl	%edi
  462013: 8b d8                        	movl	%eax, %ebx
  462015: 33 c0                        	xorl	%eax, %eax
  462017: 55                           	pushl	%ebp
  462018: 68 6e 22 46 00               	pushl	$0x46226e               # imm = 0x46226E
  46201d: 64 ff 30                     	pushl	%fs:(%eax)
  462020: 64 89 20                     	movl	%esp, %fs:(%eax)
  462023: 8d 55 fc                     	leal	-0x4(%ebp), %edx
  462026: 8b 83 54 03 00 00            	movl	0x354(%ebx), %eax
  46202c: e8 4f 14 fd ff               	calll	0x433480 <CODE+0x32480>
  462031: 83 7d fc 00                  	cmpl	$0x0, -0x4(%ebp)
  462035: 0f 84 f1 01 00 00            	je	0x46222c <CODE+0x6122c>
  46203b: 8d 55 f8                     	leal	-0x8(%ebp), %edx
  46203e: 8b 83 54 03 00 00            	movl	0x354(%ebx), %eax
  462044: e8 37 14 fd ff               	calll	0x433480 <CODE+0x32480>
  462049: 8b 45 f8                     	movl	-0x8(%ebp), %eax
  46204c: ba 84 22 46 00               	movl	$0x462284, %edx         # imm = 0x462284
  462051: e8 6a 22 fa ff               	calll	0x4042c0 <CODE+0x32c0>
  462056: 0f 86 d0 01 00 00            	jbe	0x46222c <CODE+0x6122c>
  46205c: 8d 55 f4                     	leal	-0xc(%ebp), %edx
  46205f: 8b 83 54 03 00 00            	movl	0x354(%ebx), %eax
  462065: e8 16 14 fd ff               	calll	0x433480 <CODE+0x32480>
  46206a: 8b 45 f4                     	movl	-0xc(%ebp), %eax
  46206d: e8 9a 5e fa ff               	calll	0x407f0c <CODE+0x6f0c>
  462072: a3 0c 5c 46 00               	movl	%eax, 0x465c0c
  462077: a1 0c 5c 46 00               	movl	0x465c0c, %eax
  46207c: 50                           	pushl	%eax
  46207d: b8 24 5c 46 00               	movl	$0x465c24, %eax         # imm = 0x465C24
  462082: b9 01 00 00 00               	movl	$0x1, %ecx
  462087: 8b 15 c8 01 46 00            	movl	0x4601c8, %edx
  46208d: e8 02 2e fa ff               	calll	0x404e94 <CODE+0x3e94>
  462092: 83 c4 04                     	addl	$0x4, %esp
  462095: a1 0c 5c 46 00               	movl	0x465c0c, %eax
  46209a: 50                           	pushl	%eax
  46209b: b8 28 5c 46 00               	movl	$0x465c28, %eax         # imm = 0x465C28
  4620a0: b9 01 00 00 00               	movl	$0x1, %ecx
  4620a5: 8b 15 e8 01 46 00            	movl	0x4601e8, %edx
  4620ab: e8 e4 2d fa ff               	calll	0x404e94 <CODE+0x3e94>
  4620b0: 83 c4 04                     	addl	$0x4, %esp
  4620b3: 8b 15 0c 5c 46 00            	movl	0x465c0c, %edx
  4620b9: 42                           	incl	%edx
  4620ba: 8b 83 f8 02 00 00            	movl	0x2f8(%ebx), %eax
  4620c0: e8 a3 ba ff ff               	calll	0x45db68 <CODE+0x5cb68>
  4620c5: 8b 15 0c 5c 46 00            	movl	0x465c0c, %edx
  4620cb: 83 c2 02                     	addl	$0x2, %edx
  4620ce: 8b 83 f8 02 00 00            	movl	0x2f8(%ebx), %eax
  4620d4: e8 ff b6 ff ff               	calll	0x45d7d8 <CODE+0x5c7d8>
  4620d9: 8b 15 0c 5c 46 00            	movl	0x465c0c, %edx
  4620df: 42                           	incl	%edx
  4620e0: 8b 83 fc 02 00 00            	movl	0x2fc(%ebx), %eax
  4620e6: e8 7d ba ff ff               	calll	0x45db68 <CODE+0x5cb68>
  4620eb: 8b 3d 0c 5c 46 00            	movl	0x465c0c, %edi
  4620f1: 83 c7 02                     	addl	$0x2, %edi
  4620f4: 85 ff                        	testl	%edi, %edi
  4620f6: 7e 26                        	jle	0x46211e <CODE+0x6111e>
  4620f8: be 01 00 00 00               	movl	$0x1, %esi
  4620fd: 8d 55 f0                     	leal	-0x10(%ebp), %edx
  462100: 8b c6                        	movl	%esi, %eax
  462102: e8 c9 5c fa ff               	calll	0x407dd0 <CODE+0x6dd0>
  462107: 8b 45 f0                     	movl	-0x10(%ebp), %eax
  46210a: 50                           	pushl	%eax
  46210b: 8b ce                        	movl	%esi, %ecx
  46210d: 33 d2                        	xorl	%edx, %edx
  46210f: 8b 83 f8 02 00 00            	movl	0x2f8(%ebx), %eax
  462115: e8 ca db ff ff               	calll	0x45fce4 <CODE+0x5ece4>
  46211a: 46                           	incl	%esi
  46211b: 4f                           	decl	%edi
  46211c: 75 df                        	jne	0x4620fd <CODE+0x610fd>
  46211e: 8b 3d 0c 5c 46 00            	movl	0x465c0c, %edi
  462124: 47                           	incl	%edi
  462125: 85 ff                        	testl	%edi, %edi
  462127: 7e 27                        	jle	0x462150 <CODE+0x61150>
  462129: be 01 00 00 00               	movl	$0x1, %esi
  46212e: 8d 55 ec                     	leal	-0x14(%ebp), %edx
  462131: 8b c6                        	movl	%esi, %eax
  462133: 48                           	decl	%eax
  462134: e8 97 5c fa ff               	calll	0x407dd0 <CODE+0x6dd0>
  462139: 8b 45 ec                     	movl	-0x14(%ebp), %eax
  46213c: 50                           	pushl	%eax
  46213d: 33 c9                        	xorl	%ecx, %ecx
  46213f: 8b d6                        	movl	%esi, %edx
  462141: 8b 83 f8 02 00 00            	movl	0x2f8(%ebx), %eax
  462147: e8 98 db ff ff               	calll	0x45fce4 <CODE+0x5ece4>
  46214c: 46                           	incl	%esi
  46214d: 4f                           	decl	%edi
  46214e: 75 de                        	jne	0x46212e <CODE+0x6112e>
  462150: 68 90 22 46 00               	pushl	$0x462290               # imm = 0x462290
  462155: 33 c9                        	xorl	%ecx, %ecx
  462157: 33 d2                        	xorl	%edx, %edx
  462159: 8b 83 fc 02 00 00            	movl	0x2fc(%ebx), %eax
  46215f: e8 80 db ff ff               	calll	0x45fce4 <CODE+0x5ece4>
  462164: 8d 55 e8                     	leal	-0x18(%ebp), %edx
  462167: 8b b3 00 03 00 00            	movl	0x300(%ebx), %esi
  46216d: 8b c6                        	movl	%esi, %eax
  46216f: e8 0c 13 fd ff               	calll	0x433480 <CODE+0x32480>
  462174: 8d 45 e8                     	leal	-0x18(%ebp), %eax
  462177: 50                           	pushl	%eax
  462178: 8d 55 e4                     	leal	-0x1c(%ebp), %edx
  46217b: a1 0c 5c 46 00               	movl	0x465c0c, %eax
  462180: e8 4b 5c fa ff               	calll	0x407dd0 <CODE+0x6dd0>
  462185: 8b 55 e4                     	movl	-0x1c(%ebp), %edx
  462188: 58                           	popl	%eax
  462189: e8 ee 1f fa ff               	calll	0x40417c <CODE+0x317c>
  46218e: 8b 55 e8                     	movl	-0x18(%ebp), %edx
  462191: 8b c6                        	movl	%esi, %eax
  462193: e8 18 13 fd ff               	calll	0x4334b0 <CODE+0x324b0>
  462198: ba 9c 22 46 00               	movl	$0x46229c, %edx         # imm = 0x46229C
  46219d: 8b 83 14 03 00 00            	movl	0x314(%ebx), %eax
  4621a3: e8 08 13 fd ff               	calll	0x4334b0 <CODE+0x324b0>
  4621a8: 33 d2                        	xorl	%edx, %edx
  4621aa: 8b 83 54 03 00 00            	movl	0x354(%ebx), %eax
  4621b0: e8 eb 11 fd ff               	calll	0x4333a0 <CODE+0x323a0>
  4621b5: 33 d2                        	xorl	%edx, %edx
  4621b7: 8b 83 58 03 00 00            	movl	0x358(%ebx), %eax
  4621bd: e8 de 11 fd ff               	calll	0x4333a0 <CODE+0x323a0>
  4621c2: b2 01                        	movb	$0x1, %dl
  4621c4: 8b 83 00 03 00 00            	movl	0x300(%ebx), %eax
  4621ca: e8 d1 11 fd ff               	calll	0x4333a0 <CODE+0x323a0>
  4621cf: b2 01                        	movb	$0x1, %dl
  4621d1: 8b 83 04 03 00 00            	movl	0x304(%ebx), %eax
  4621d7: e8 c4 11 fd ff               	calll	0x4333a0 <CODE+0x323a0>
  4621dc: b2 01                        	movb	$0x1, %dl
  4621de: 8b 83 08 03 00 00            	movl	0x308(%ebx), %eax
  4621e4: e8 b7 11 fd ff               	calll	0x4333a0 <CODE+0x323a0>
  4621e9: b2 01                        	movb	$0x1, %dl
  4621eb: 8b 83 18 03 00 00            	movl	0x318(%ebx), %eax
  4621f1: e8 aa 11 fd ff               	calll	0x4333a0 <CODE+0x323a0>
  4621f6: b2 01                        	movb	$0x1, %dl
  4621f8: 8b 83 0c 03 00 00            	movl	0x30c(%ebx), %eax
  4621fe: e8 9d 11 fd ff               	calll	0x4333a0 <CODE+0x323a0>
  462203: b2 01                        	movb	$0x1, %dl
  462205: 8b 83 10 03 00 00            	movl	0x310(%ebx), %eax
  46220b: e8 90 11 fd ff               	calll	0x4333a0 <CODE+0x323a0>
  462210: b2 01                        	movb	$0x1, %dl
  462212: 8b 83 f8 02 00 00            	movl	0x2f8(%ebx), %eax
  462218: e8 83 11 fd ff               	calll	0x4333a0 <CODE+0x323a0>
  46221d: b2 01                        	movb	$0x1, %dl
  46221f: 8b 83 fc 02 00 00            	movl	0x2fc(%ebx), %eax
  462225: e8 76 11 fd ff               	calll	0x4333a0 <CODE+0x323a0>
  46222a: eb 0a                        	jmp	0x462236 <CODE+0x61236>
  46222c: b8 bc 22 46 00               	movl	$0x4622bc, %eax         # imm = 0x4622BC
  462231: e8 f6 54 fc ff               	calll	0x42772c <CODE+0x2672c>
  462236: 33 c0                        	xorl	%eax, %eax
  462238: 5a                           	popl	%edx
  462239: 59                           	popl	%ecx
  46223a: 59                           	popl	%ecx
  46223b: 64 89 10                     	movl	%edx, %fs:(%eax)
  46223e: 68 75 22 46 00               	pushl	$0x462275               # imm = 0x462275
  462243: 8d 45 e4                     	leal	-0x1c(%ebp), %eax
  462246: e8 69 1c fa ff               	calll	0x403eb4 <CODE+0x2eb4>
  46224b: 8d 45 e8                     	leal	-0x18(%ebp), %eax
  46224e: e8 61 1c fa ff               	calll	0x403eb4 <CODE+0x2eb4>
  462253: 8d 45 ec                     	leal	-0x14(%ebp), %eax
  462256: ba 02 00 00 00               	movl	$0x2, %edx
  46225b: e8 78 1c fa ff               	calll	0x403ed8 <CODE+0x2ed8>
  462260: 8d 45 f4                     	leal	-0xc(%ebp), %eax
  462263: ba 03 00 00 00               	movl	$0x3, %edx
  462268: e8 6b 1c fa ff               	calll	0x403ed8 <CODE+0x2ed8>
  46226d: c3                           	retl
  46226e: e9 45 16 fa ff               	jmp	0x4038b8 <CODE+0x28b8>
  462273: eb ce                        	jmp	0x462243 <CODE+0x61243>
  462275: 5f                           	popl	%edi
  462276: 5e                           	popl	%esi
  462277: 5b                           	popl	%ebx
  462278: 8b e5                        	movl	%ebp, %esp
  46227a: 5d                           	popl	%ebp
  46227b: c3                           	retl
  46227c: ff ff                        	<unknown>
  46227e: ff ff                        	<unknown>
  462280: 01 00                        	addl	%eax, (%eax)
  462282: 00 00                        	addb	%al, (%eax)
  462284: 30 00                        	xorb	%al, (%eax)
  462286: 00 00                        	addb	%al, (%eax)
  462288: ff ff                        	<unknown>
  46228a: ff ff                        	<unknown>
  46228c: 02 00                        	addb	(%eax), %al
  46228e: 00 00                        	addb	%al, (%eax)
  462290: 41                           	incl	%ecx
  462291: 6a 00                        	pushl	$0x0
  462293: 00 ff                        	addb	%bh, %bh
  462295: ff ff                        	<unknown>
  462297: ff 14 00                     	calll	*(%eax,%eax)
  46229a: 00 00                        	addb	%al, (%eax)
  46229c: c2 e2 e5                     	retl	$-0x1a1e                # imm = 0xE5E2
  46229f: e4 e8                        	inb	$0xe8, %al
  4622a1: f2 e5 20                     	repne		inl	$0x20, %eax
  4622a4: e2 e0                        	loop	0x462286 <CODE+0x61286>
  4622a6: f8                           	clc
  4622a7: e8 20 e4 e0 ed               	calll	0xee2706cc
  4622ac: ed                           	inl	%dx, %eax
  4622ad: fb                           	sti
  4622ae: e5 3a                        	inl	$0x3a, %eax
  4622b0: 00 00                        	addb	%al, (%eax)
  4622b2: 00 00                        	addb	%al, (%eax)
  4622b4: ff ff                        	<unknown>
  4622b6: ff ff                        	<unknown>
  4622b8: 28 00                        	subb	%al, (%eax)
  4622ba: 00 00                        	addb	%al, (%eax)
  4622bc: cf                           	iretl
  4622bd: f0                           	lock
  4622be: ee                           	outb	%al, %dx
  4622bf: e2 e5                        	loop	0x4622a6 <CODE+0x612a6>
  4622c1: f0                           	lock
  4622c2: fc                           	cld
  4622c3: f2 e5 20                     	repne		inl	$0x20, %eax
  4622c6: ef                           	outl	%eax, %dx
  4622c7: f0                           	lock
  4622c8: e0 e2                        	loopne	0x4622ac <CODE+0x612ac>
  4622ca: e8 eb fc ed ee               	calll	0xef341fba
  4622cf: f1                           	<unknown>
  4622d0: f2 fc                        	repne		cld
  4622d2: 20 e2                        	andb	%ah, %dl
  4622d4: e2 e5                        	loop	0x4622bb <CODE+0x612bb>
  4622d6: e4 e5                        	inb	$0xe5, %al
  4622d8: ed                           	inl	%dx, %eax
  4622d9: ed                           	inl	%dx, %eax
  4622da: fb                           	sti
  4622db: f5                           	cmc
  4622dc: 20 e4                        	andb	%ah, %ah
  4622de: e0 ed                        	loopne	0x4622cd <CODE+0x612cd>
  4622e0: ed                           	inl	%dx, %eax
  4622e1: fb                           	sti
  4622e2: f5                           	cmc
  4622e3: 21 00                        	andl	%eax, (%eax)
  4622e5: 00 00                        	addb	%al, (%eax)
  4622e7: 00 55 8b                     	addb	%dl, -0x75(%ebp)
  4622ea: ec                           	inb	%dx, %al
  4622eb: 33 c0                        	xorl	%eax, %eax
  4622ed: 55                           	pushl	%ebp
  4622ee: 68 7f 23 46 00               	pushl	$0x46237f               # imm = 0x46237F
  4622f3: 64 ff 30                     	pushl	%fs:(%eax)
  4622f6: 64 89 20                     	movl	%esp, %fs:(%eax)
  4622f9: ff 05 44 5c 46 00            	incl	0x465c44
  4622ff: 75 70                        	jne	0x462371 <CODE+0x61371>
  462301: b8 34 5c 46 00               	movl	$0x465c34, %eax         # imm = 0x465C34
  462306: 8b 15 68 02 46 00            	movl	0x460268, %edx
  46230c: e8 8f 2b fa ff               	calll	0x404ea0 <CODE+0x3ea0>
  462311: b8 30 5c 46 00               	movl	$0x465c30, %eax         # imm = 0x465C30
  462316: 8b 15 28 02 46 00            	movl	0x460228, %edx
