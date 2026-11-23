
/Users/cassidal/Documents/vuz/tiger/source/Лаб_3/Загрузка_рюкзака.exe:	file format coff-i386

Disassembly of section CODE:

00401000 <CODE>:
  46137c: 55                           	pushl	%ebp
  46137d: 8b ec                        	movl	%esp, %ebp
  46137f: b9 0a 00 00 00               	movl	$0xa, %ecx
  461384: 6a 00                        	pushl	$0x0
  461386: 6a 00                        	pushl	$0x0
  461388: 49                           	decl	%ecx
  461389: 75 f9                        	jne	0x461384 <CODE+0x60384>
  46138b: 51                           	pushl	%ecx
  46138c: 53                           	pushl	%ebx
  46138d: 56                           	pushl	%esi
  46138e: 57                           	pushl	%edi
  46138f: 8b f8                        	movl	%eax, %edi
  461391: 33 c0                        	xorl	%eax, %eax
  461393: 55                           	pushl	%ebp
  461394: 68 cf 19 46 00               	pushl	$0x4619cf               # imm = 0x4619CF
  461399: 64 ff 30                     	pushl	%fs:(%eax)
  46139c: 64 89 20                     	movl	%esp, %fs:(%eax)
  46139f: c6 45 f7 01                  	movb	$0x1, -0x9(%ebp)
  4613a3: 6a 02                        	pushl	$0x2
  4613a5: 8d 45 f8                     	leal	-0x8(%ebp), %eax
  4613a8: b9 01 00 00 00               	movl	$0x1, %ecx
  4613ad: 8b 15 5c 13 46 00            	movl	0x46135c, %edx
  4613b3: e8 dc 3a fa ff               	calll	0x404e94 <CODE+0x3e94>
  4613b8: 83 c4 04                     	addl	$0x4, %esp
  4613bb: 33 db                        	xorl	%ebx, %ebx
  4613bd: 8b 87 28 03 00 00            	movl	0x328(%edi), %eax
  4613c3: 8b 80 4c 02 00 00            	movl	0x24c(%eax), %eax
  4613c9: 48                           	decl	%eax
  4613ca: 50                           	pushl	%eax
  4613cb: 8b 45 f8                     	movl	-0x8(%ebp), %eax
  4613ce: 8d 04 98                     	leal	(%eax,%ebx,4), %eax
  4613d1: b9 01 00 00 00               	movl	$0x1, %ecx
  4613d6: 8b 15 3c 13 46 00            	movl	0x46133c, %edx
  4613dc: e8 b3 3a fa ff               	calll	0x404e94 <CODE+0x3e94>
  4613e1: 83 c4 04                     	addl	$0x4, %esp
  4613e4: 8b 87 28 03 00 00            	movl	0x328(%edi), %eax
  4613ea: 8b 80 4c 02 00 00            	movl	0x24c(%eax), %eax
  4613f0: 83 e8 02                     	subl	$0x2, %eax
  4613f3: 85 c0                        	testl	%eax, %eax
  4613f5: 7c 5a                        	jl	0x461451 <CODE+0x60451>
  4613f7: 40                           	incl	%eax
  4613f8: 89 45 f0                     	movl	%eax, -0x10(%ebp)
  4613fb: 33 f6                        	xorl	%esi, %esi
  4613fd: 8d 45 e4                     	leal	-0x1c(%ebp), %eax
  461400: 50                           	pushl	%eax
  461401: 8d 4e 01                     	leal	0x1(%esi), %ecx
  461404: 8b 87 28 03 00 00            	movl	0x328(%edi), %eax
  46140a: 8b d3                        	movl	%ebx, %edx
  46140c: e8 63 e8 ff ff               	calll	0x45fc74 <CODE+0x5ec74>
  461411: 83 7d e4 00                  	cmpl	$0x0, -0x1c(%ebp)
  461415: 75 0f                        	jne	0x461426 <CODE+0x60426>
  461417: 8b 45 f8                     	movl	-0x8(%ebp), %eax
  46141a: 8b 04 98                     	movl	(%eax,%ebx,4), %eax
  46141d: c7 04 b0 ff ff ff ff         	movl	$0xffffffff, (%eax,%esi,4) # imm = 0xFFFFFFFF
  461424: eb 25                        	jmp	0x46144b <CODE+0x6044b>
  461426: 8d 45 e0                     	leal	-0x20(%ebp), %eax
  461429: 50                           	pushl	%eax
  46142a: 8d 4e 01                     	leal	0x1(%esi), %ecx
  46142d: 8b 87 28 03 00 00            	movl	0x328(%edi), %eax
  461433: 8b d3                        	movl	%ebx, %edx
  461435: e8 3a e8 ff ff               	calll	0x45fc74 <CODE+0x5ec74>
  46143a: 8b 45 e0                     	movl	-0x20(%ebp), %eax
  46143d: e8 ca 6a fa ff               	calll	0x407f0c <CODE+0x6f0c>
  461442: 8b 55 f8                     	movl	-0x8(%ebp), %edx
  461445: 8b 14 9a                     	movl	(%edx,%ebx,4), %edx
  461448: 89 04 b2                     	movl	%eax, (%edx,%esi,4)
  46144b: 46                           	incl	%esi
  46144c: ff 4d f0                     	decl	-0x10(%ebp)
  46144f: 75 ac                        	jne	0x4613fd <CODE+0x603fd>
  461451: 43                           	incl	%ebx
  461452: 83 fb 02                     	cmpl	$0x2, %ebx
  461455: 0f 85 62 ff ff ff            	jne	0x4613bd <CODE+0x603bd>
  46145b: 83 3d 18 5c 46 00 01         	cmpl	$0x1, 0x465c18
  461462: 0f 84 bf 00 00 00            	je	0x461527 <CODE+0x60527>
  461468: 8b 87 28 03 00 00            	movl	0x328(%edi), %eax
  46146e: 8b 80 4c 02 00 00            	movl	0x24c(%eax), %eax
  461474: 83 e8 02                     	subl	$0x2, %eax
  461477: 85 c0                        	testl	%eax, %eax
  461479: 7c 48                        	jl	0x4614c3 <CODE+0x604c3>
  46147b: 40                           	incl	%eax
  46147c: 89 45 f0                     	movl	%eax, -0x10(%ebp)
  46147f: 33 db                        	xorl	%ebx, %ebx
  461481: a1 0c 5c 46 00               	movl	0x465c0c, %eax
  461486: 2b 05 18 5c 46 00            	subl	0x465c18, %eax
  46148c: 8b 15 2c 5c 46 00            	movl	0x465c2c, %edx
  461492: 8b 14 82                     	movl	(%edx,%eax,4), %edx
  461495: 8b 14 9a                     	movl	(%edx,%ebx,4), %edx
  461498: 8b 4d f8                     	movl	-0x8(%ebp), %ecx
  46149b: 8b 09                        	movl	(%ecx), %ecx
  46149d: 3b 14 99                     	cmpl	(%ecx,%ebx,4), %edx
  4614a0: 75 17                        	jne	0x4614b9 <CODE+0x604b9>
  4614a2: 8b 15 30 5c 46 00            	movl	0x465c30, %edx
  4614a8: 8b 04 82                     	movl	(%edx,%eax,4), %eax
  4614ab: 8b 04 98                     	movl	(%eax,%ebx,4), %eax
  4614ae: 8b 55 f8                     	movl	-0x8(%ebp), %edx
  4614b1: 8b 52 04                     	movl	0x4(%edx), %edx
  4614b4: 3b 04 9a                     	cmpl	(%edx,%ebx,4), %eax
  4614b7: 74 04                        	je	0x4614bd <CODE+0x604bd>
  4614b9: c6 45 f7 00                  	movb	$0x0, -0x9(%ebp)
  4614bd: 43                           	incl	%ebx
  4614be: ff 4d f0                     	decl	-0x10(%ebp)
  4614c1: 75 be                        	jne	0x461481 <CODE+0x60481>
  4614c3: 80 7d f7 00                  	cmpb	$0x0, -0x9(%ebp)
  4614c7: 74 49                        	je	0x461512 <CODE+0x60512>
  4614c9: b8 e8 19 46 00               	movl	$0x4619e8, %eax         # imm = 0x4619E8
  4614ce: e8 59 62 fc ff               	calll	0x42772c <CODE+0x2672c>
  4614d3: 8b 87 48 03 00 00            	movl	0x348(%edi), %eax
  4614d9: 33 d2                        	xorl	%edx, %edx
  4614db: e8 c0 1e fd ff               	calll	0x4333a0 <CODE+0x323a0>
  4614e0: 8b 87 14 03 00 00            	movl	0x314(%edi), %eax
  4614e6: 33 d2                        	xorl	%edx, %edx
  4614e8: e8 b3 1e fd ff               	calll	0x4333a0 <CODE+0x323a0>
  4614ed: ff 0d 18 5c 46 00            	decl	0x465c18
  4614f3: 8b 87 38 03 00 00            	movl	0x338(%edi), %eax
  4614f9: 33 d2                        	xorl	%edx, %edx
  4614fb: e8 a0 1e fd ff               	calll	0x4333a0 <CODE+0x323a0>
  461500: 8b 87 1c 03 00 00            	movl	0x31c(%edi), %eax
  461506: b2 01                        	movb	$0x1, %dl
  461508: e8 93 1e fd ff               	calll	0x4333a0 <CODE+0x323a0>
  46150d: e9 94 04 00 00               	jmp	0x4619a6 <CODE+0x609a6>
  461512: ff 05 40 5c 46 00            	incl	0x465c40
  461518: b8 fc 19 46 00               	movl	$0x4619fc, %eax         # imm = 0x4619FC
  46151d: e8 0a 62 fc ff               	calll	0x42772c <CODE+0x2672c>
  461522: e9 7f 04 00 00               	jmp	0x4619a6 <CODE+0x609a6>
  461527: 8b 87 28 03 00 00            	movl	0x328(%edi), %eax
  46152d: 8b 80 4c 02 00 00            	movl	0x24c(%eax), %eax
  461533: 83 e8 02                     	subl	$0x2, %eax
  461536: 85 c0                        	testl	%eax, %eax
  461538: 7c 5e                        	jl	0x461598 <CODE+0x60598>
  46153a: 40                           	incl	%eax
  46153b: 89 45 f0                     	movl	%eax, -0x10(%ebp)
  46153e: 33 db                        	xorl	%ebx, %ebx
  461540: 8b 0d 0c 5c 46 00            	movl	0x465c0c, %ecx
  461546: 2b 0d 18 5c 46 00            	subl	0x465c18, %ecx
  46154c: 8b 35 2c 5c 46 00            	movl	0x465c2c, %esi
  461552: 8b 0c 8e                     	movl	(%esi,%ecx,4), %ecx
  461555: 8b 0c 99                     	movl	(%ecx,%ebx,4), %ecx
  461558: 8b 45 f8                     	movl	-0x8(%ebp), %eax
  46155b: 8b 00                        	movl	(%eax), %eax
  46155d: 8b 04 98                     	movl	(%eax,%ebx,4), %eax
  461560: 3b c8                        	cmpl	%eax, %ecx
  461562: 74 03                        	je	0x461567 <CODE+0x60567>
  461564: 40                           	incl	%eax
  461565: 75 27                        	jne	0x46158e <CODE+0x6058e>
  461567: a1 0c 5c 46 00               	movl	0x465c0c, %eax
  46156c: 2b 05 18 5c 46 00            	subl	0x465c18, %eax
  461572: 8b 0d 30 5c 46 00            	movl	0x465c30, %ecx
  461578: 8b 04 81                     	movl	(%ecx,%eax,4), %eax
  46157b: 8b 04 98                     	movl	(%eax,%ebx,4), %eax
  46157e: 8b 55 f8                     	movl	-0x8(%ebp), %edx
  461581: 8b 52 04                     	movl	0x4(%edx), %edx
  461584: 8b 14 9a                     	movl	(%edx,%ebx,4), %edx
  461587: 3b c2                        	cmpl	%edx, %eax
  461589: 74 07                        	je	0x461592 <CODE+0x60592>
  46158b: 42                           	incl	%edx
  46158c: 74 04                        	je	0x461592 <CODE+0x60592>
  46158e: c6 45 f7 00                  	movb	$0x0, -0x9(%ebp)
  461592: 43                           	incl	%ebx
  461593: ff 4d f0                     	decl	-0x10(%ebp)
  461596: 75 a8                        	jne	0x461540 <CODE+0x60540>
  461598: 80 7d f7 00                  	cmpb	$0x0, -0x9(%ebp)
  46159c: 0f 84 04 04 00 00            	je	0x4619a6 <CODE+0x609a6>
  4615a2: b8 e8 19 46 00               	movl	$0x4619e8, %eax         # imm = 0x4619E8
  4615a7: e8 80 61 fc ff               	calll	0x42772c <CODE+0x2672c>
  4615ac: ff 0d 18 5c 46 00            	decl	0x465c18
  4615b2: 8b 87 38 03 00 00            	movl	0x338(%edi), %eax
  4615b8: 33 d2                        	xorl	%edx, %edx
  4615ba: e8 e1 1d fd ff               	calll	0x4333a0 <CODE+0x323a0>
  4615bf: 8b 87 3c 03 00 00            	movl	0x33c(%edi), %eax
  4615c5: b2 01                        	movb	$0x1, %dl
  4615c7: e8 d4 1d fd ff               	calll	0x4333a0 <CODE+0x323a0>
  4615cc: 8b 87 14 03 00 00            	movl	0x314(%edi), %eax
  4615d2: ba 2c 1a 46 00               	movl	$0x461a2c, %edx         # imm = 0x461A2C
  4615d7: e8 d4 1e fd ff               	calll	0x4334b0 <CODE+0x324b0>
  4615dc: 8b 87 48 03 00 00            	movl	0x348(%edi), %eax
  4615e2: 33 d2                        	xorl	%edx, %edx
  4615e4: e8 b7 1d fd ff               	calll	0x4333a0 <CODE+0x323a0>
  4615e9: 8b 87 30 03 00 00            	movl	0x330(%edi), %eax
  4615ef: b2 01                        	movb	$0x1, %dl
  4615f1: e8 aa 1d fd ff               	calll	0x4333a0 <CODE+0x323a0>
  4615f6: 8b 87 2c 03 00 00            	movl	0x32c(%edi), %eax
  4615fc: b2 01                        	movb	$0x1, %dl
  4615fe: e8 9d 1d fd ff               	calll	0x4333a0 <CODE+0x323a0>
  461603: 8b 15 0c 5c 46 00            	movl	0x465c0c, %edx
  461609: 42                           	incl	%edx
  46160a: 8b 87 2c 03 00 00            	movl	0x32c(%edi), %eax
  461610: e8 53 c5 ff ff               	calll	0x45db68 <CODE+0x5cb68>
  461615: 68 5c 1a 46 00               	pushl	$0x461a5c               # imm = 0x461A5C
  46161a: 8b 87 2c 03 00 00            	movl	0x32c(%edi), %eax
  461620: 33 c9                        	xorl	%ecx, %ecx
  461622: ba 01 00 00 00               	movl	$0x1, %edx
  461627: e8 b8 e6 ff ff               	calll	0x45fce4 <CODE+0x5ece4>
  46162c: 68 68 1a 46 00               	pushl	$0x461a68               # imm = 0x461A68
  461631: 8b 87 2c 03 00 00            	movl	0x32c(%edi), %eax
  461637: 33 c9                        	xorl	%ecx, %ecx
  461639: ba 02 00 00 00               	movl	$0x2, %edx
  46163e: e8 a1 e6 ff ff               	calll	0x45fce4 <CODE+0x5ece4>
  461643: a1 0c 5c 46 00               	movl	0x465c0c, %eax
  461648: 85 c0                        	testl	%eax, %eax
  46164a: 7e 2b                        	jle	0x461677 <CODE+0x60677>
  46164c: 89 45 f0                     	movl	%eax, -0x10(%ebp)
  46164f: bb 01 00 00 00               	movl	$0x1, %ebx
  461654: 8d 55 dc                     	leal	-0x24(%ebp), %edx
  461657: 8b c3                        	movl	%ebx, %eax
  461659: e8 72 67 fa ff               	calll	0x407dd0 <CODE+0x6dd0>
  46165e: 8b 45 dc                     	movl	-0x24(%ebp), %eax
  461661: 50                           	pushl	%eax
  461662: 8b 87 2c 03 00 00            	movl	0x32c(%edi), %eax
  461668: 8b cb                        	movl	%ebx, %ecx
  46166a: 33 d2                        	xorl	%edx, %edx
  46166c: e8 73 e6 ff ff               	calll	0x45fce4 <CODE+0x5ece4>
  461671: 43                           	incl	%ebx
  461672: ff 4d f0                     	decl	-0x10(%ebp)
  461675: 75 dd                        	jne	0x461654 <CODE+0x60654>
  461677: 8b 15 0c 5c 46 00            	movl	0x465c0c, %edx
  46167d: 83 c2 02                     	addl	$0x2, %edx
  461680: 8b 87 24 03 00 00            	movl	0x324(%edi), %eax
  461686: e8 4d c1 ff ff               	calll	0x45d7d8 <CODE+0x5c7d8>
  46168b: 8b 15 14 5c 46 00            	movl	0x465c14, %edx
  461691: 83 c2 04                     	addl	$0x4, %edx
  461694: 0f af 15 0c 5c 46 00         	imull	0x465c0c, %edx
  46169b: 8b 87 24 03 00 00            	movl	0x324(%edi), %eax
  4616a1: e8 c2 c4 ff ff               	calll	0x45db68 <CODE+0x5cb68>
  4616a6: 8b 87 24 03 00 00            	movl	0x324(%edi), %eax
  4616ac: 33 d2                        	xorl	%edx, %edx
  4616ae: e8 51 c3 ff ff               	calll	0x45da04 <CODE+0x5ca04>
  4616b3: a1 0c 5c 46 00               	movl	0x465c0c, %eax
  4616b8: 83 e8 02                     	subl	$0x2, %eax
  4616bb: 85 c0                        	testl	%eax, %eax
  4616bd: 0f 8c f2 00 00 00            	jl	0x4617b5 <CODE+0x607b5>
  4616c3: 40                           	incl	%eax
  4616c4: 89 45 f0                     	movl	%eax, -0x10(%ebp)
  4616c7: c7 45 fc 00 00 00 00         	movl	$0x0, -0x4(%ebp)
  4616ce: 8d 55 d4                     	leal	-0x2c(%ebp), %edx
  4616d1: 8b 45 fc                     	movl	-0x4(%ebp), %eax
  4616d4: 40                           	incl	%eax
  4616d5: e8 f6 66 fa ff               	calll	0x407dd0 <CODE+0x6dd0>
  4616da: 8b 4d d4                     	movl	-0x2c(%ebp), %ecx
  4616dd: 8d 45 d8                     	leal	-0x28(%ebp), %eax
  4616e0: ba 74 1a 46 00               	movl	$0x461a74, %edx         # imm = 0x461A74
  4616e5: e8 d6 2a fa ff               	calll	0x4041c0 <CODE+0x31c0>
  4616ea: 8b 45 d8                     	movl	-0x28(%ebp), %eax
  4616ed: 50                           	pushl	%eax
  4616ee: 8b 0d 14 5c 46 00            	movl	0x465c14, %ecx
  4616f4: 83 c1 03                     	addl	$0x3, %ecx
  4616f7: 0f af 4d fc                  	imull	-0x4(%ebp), %ecx
  4616fb: 8b 87 24 03 00 00            	movl	0x324(%edi), %eax
  461701: 33 d2                        	xorl	%edx, %edx
  461703: e8 dc e5 ff ff               	calll	0x45fce4 <CODE+0x5ece4>
  461708: a1 14 5c 46 00               	movl	0x465c14, %eax
  46170d: 85 c0                        	testl	%eax, %eax
  46170f: 0f 8c 94 00 00 00            	jl	0x4617a9 <CODE+0x607a9>
  461715: 40                           	incl	%eax
  461716: 89 45 ec                     	movl	%eax, -0x14(%ebp)
  461719: 33 db                        	xorl	%ebx, %ebx
  46171b: a1 28 5c 46 00               	movl	0x465c28, %eax
  461720: 8b 55 fc                     	movl	-0x4(%ebp), %edx
  461723: 8b 04 90                     	movl	(%eax,%edx,4), %eax
  461726: 83 e8 02                     	subl	$0x2, %eax
  461729: 85 c0                        	testl	%eax, %eax
  46172b: 7c 72                        	jl	0x46179f <CODE+0x6079f>
  46172d: 40                           	incl	%eax
  46172e: 89 45 e8                     	movl	%eax, -0x18(%ebp)
  461731: 33 f6                        	xorl	%esi, %esi
  461733: a1 24 5c 46 00               	movl	0x465c24, %eax
  461738: 8b 55 fc                     	movl	-0x4(%ebp), %edx
  46173b: 8b 04 90                     	movl	(%eax,%edx,4), %eax
  46173e: 8b 04 98                     	movl	(%eax,%ebx,4), %eax
  461741: 8b 04 b0                     	movl	(%eax,%esi,4), %eax
  461744: 8d 55 d0                     	leal	-0x30(%ebp), %edx
  461747: e8 84 66 fa ff               	calll	0x407dd0 <CODE+0x6dd0>
  46174c: 8b 45 d0                     	movl	-0x30(%ebp), %eax
  46174f: 50                           	pushl	%eax
  461750: 8b 0d 14 5c 46 00            	movl	0x465c14, %ecx
  461756: 83 c1 03                     	addl	$0x3, %ecx
  461759: 0f af 4d fc                  	imull	-0x4(%ebp), %ecx
  46175d: 03 cb                        	addl	%ebx, %ecx
  46175f: 41                           	incl	%ecx
  461760: 8d 56 01                     	leal	0x1(%esi), %edx
  461763: 8b 87 24 03 00 00            	movl	0x324(%edi), %eax
  461769: e8 76 e5 ff ff               	calll	0x45fce4 <CODE+0x5ece4>
  46176e: 8d 55 cc                     	leal	-0x34(%ebp), %edx
  461771: 8b c3                        	movl	%ebx, %eax
  461773: e8 58 66 fa ff               	calll	0x407dd0 <CODE+0x6dd0>
  461778: 8b 45 cc                     	movl	-0x34(%ebp), %eax
  46177b: 50                           	pushl	%eax
  46177c: 8b 0d 14 5c 46 00            	movl	0x465c14, %ecx
  461782: 83 c1 03                     	addl	$0x3, %ecx
  461785: 0f af 4d fc                  	imull	-0x4(%ebp), %ecx
  461789: 03 cb                        	addl	%ebx, %ecx
  46178b: 41                           	incl	%ecx
  46178c: 8b 87 24 03 00 00            	movl	0x324(%edi), %eax
  461792: 33 d2                        	xorl	%edx, %edx
  461794: e8 4b e5 ff ff               	calll	0x45fce4 <CODE+0x5ece4>
  461799: 46                           	incl	%esi
  46179a: ff 4d e8                     	decl	-0x18(%ebp)
  46179d: 75 94                        	jne	0x461733 <CODE+0x60733>
  46179f: 43                           	incl	%ebx
  4617a0: ff 4d ec                     	decl	-0x14(%ebp)
  4617a3: 0f 85 72 ff ff ff            	jne	0x46171b <CODE+0x6071b>
  4617a9: ff 45 fc                     	incl	-0x4(%ebp)
  4617ac: ff 4d f0                     	decl	-0x10(%ebp)
  4617af: 0f 85 19 ff ff ff            	jne	0x4616ce <CODE+0x606ce>
  4617b5: 8d 55 c4                     	leal	-0x3c(%ebp), %edx
  4617b8: a1 0c 5c 46 00               	movl	0x465c0c, %eax
  4617bd: e8 0e 66 fa ff               	calll	0x407dd0 <CODE+0x6dd0>
  4617c2: 8b 4d c4                     	movl	-0x3c(%ebp), %ecx
  4617c5: 8d 45 c8                     	leal	-0x38(%ebp), %eax
  4617c8: ba 74 1a 46 00               	movl	$0x461a74, %edx         # imm = 0x461A74
  4617cd: e8 ee 29 fa ff               	calll	0x4041c0 <CODE+0x31c0>
  4617d2: 8b 45 c8                     	movl	-0x38(%ebp), %eax
  4617d5: 50                           	pushl	%eax
  4617d6: 8b 0d 0c 5c 46 00            	movl	0x465c0c, %ecx
  4617dc: 49                           	decl	%ecx
  4617dd: a1 14 5c 46 00               	movl	0x465c14, %eax
  4617e2: 83 c0 03                     	addl	$0x3, %eax
  4617e5: 0f af c8                     	imull	%eax, %ecx
  4617e8: 8b 87 24 03 00 00            	movl	0x324(%edi), %eax
  4617ee: 33 d2                        	xorl	%edx, %edx
  4617f0: e8 ef e4 ff ff               	calll	0x45fce4 <CODE+0x5ece4>
  4617f5: a1 14 5c 46 00               	movl	0x465c14, %eax
  4617fa: 83 e8 03                     	subl	$0x3, %eax
  4617fd: 85 c0                        	testl	%eax, %eax
  4617ff: 0f 8c 94 00 00 00            	jl	0x461899 <CODE+0x60899>
  461805: 40                           	incl	%eax
  461806: 89 45 f0                     	movl	%eax, -0x10(%ebp)
  461809: 33 db                        	xorl	%ebx, %ebx
  46180b: a1 28 5c 46 00               	movl	0x465c28, %eax
  461810: 8b 55 fc                     	movl	-0x4(%ebp), %edx
  461813: 8b 04 90                     	movl	(%eax,%edx,4), %eax
  461816: 83 e8 02                     	subl	$0x2, %eax
  461819: 85 c0                        	testl	%eax, %eax
  46181b: 7c 72                        	jl	0x46188f <CODE+0x6088f>
  46181d: 40                           	incl	%eax
  46181e: 89 45 ec                     	movl	%eax, -0x14(%ebp)
  461821: 33 f6                        	xorl	%esi, %esi
  461823: a1 24 5c 46 00               	movl	0x465c24, %eax
  461828: 8b 55 fc                     	movl	-0x4(%ebp), %edx
  46182b: 8b 04 90                     	movl	(%eax,%edx,4), %eax
  46182e: 8b 04 98                     	movl	(%eax,%ebx,4), %eax
  461831: 8b 04 b0                     	movl	(%eax,%esi,4), %eax
  461834: 8d 55 c0                     	leal	-0x40(%ebp), %edx
  461837: e8 94 65 fa ff               	calll	0x407dd0 <CODE+0x6dd0>
  46183c: 8b 45 c0                     	movl	-0x40(%ebp), %eax
  46183f: 50                           	pushl	%eax
  461840: 8b 0d 14 5c 46 00            	movl	0x465c14, %ecx
  461846: 83 c1 03                     	addl	$0x3, %ecx
  461849: 0f af 4d fc                  	imull	-0x4(%ebp), %ecx
  46184d: 03 cb                        	addl	%ebx, %ecx
  46184f: 41                           	incl	%ecx
  461850: 8d 56 01                     	leal	0x1(%esi), %edx
  461853: 8b 87 24 03 00 00            	movl	0x324(%edi), %eax
  461859: e8 86 e4 ff ff               	calll	0x45fce4 <CODE+0x5ece4>
  46185e: 8d 55 bc                     	leal	-0x44(%ebp), %edx
  461861: 8b c3                        	movl	%ebx, %eax
  461863: e8 68 65 fa ff               	calll	0x407dd0 <CODE+0x6dd0>
  461868: 8b 45 bc                     	movl	-0x44(%ebp), %eax
  46186b: 50                           	pushl	%eax
  46186c: 8b 0d 14 5c 46 00            	movl	0x465c14, %ecx
  461872: 83 c1 03                     	addl	$0x3, %ecx
  461875: 0f af 4d fc                  	imull	-0x4(%ebp), %ecx
  461879: 03 cb                        	addl	%ebx, %ecx
  46187b: 41                           	incl	%ecx
  46187c: 8b 87 24 03 00 00            	movl	0x324(%edi), %eax
  461882: 33 d2                        	xorl	%edx, %edx
  461884: e8 5b e4 ff ff               	calll	0x45fce4 <CODE+0x5ece4>
  461889: 46                           	incl	%esi
  46188a: ff 4d ec                     	decl	-0x14(%ebp)
  46188d: 75 94                        	jne	0x461823 <CODE+0x60823>
  46188f: 43                           	incl	%ebx
  461890: ff 4d f0                     	decl	-0x10(%ebp)
  461893: 0f 85 72 ff ff ff            	jne	0x46180b <CODE+0x6080b>
  461899: 8b 15 14 5c 46 00            	movl	0x465c14, %edx
  46189f: 83 c2 04                     	addl	$0x4, %edx
  4618a2: 0f af 15 0c 5c 46 00         	imull	0x465c0c, %edx
  4618a9: 8b 87 28 03 00 00            	movl	0x328(%edi), %eax
  4618af: e8 b4 c2 ff ff               	calll	0x45db68 <CODE+0x5cb68>
  4618b4: 8b 87 24 03 00 00            	movl	0x324(%edi), %eax
  4618ba: 33 d2                        	xorl	%edx, %edx
  4618bc: e8 43 c1 ff ff               	calll	0x45da04 <CODE+0x5ca04>
  4618c1: a1 0c 5c 46 00               	movl	0x465c0c, %eax
  4618c6: 48                           	decl	%eax
  4618c7: 85 c0                        	testl	%eax, %eax
  4618c9: 0f 8c d7 00 00 00            	jl	0x4619a6 <CODE+0x609a6>
  4618cf: 40                           	incl	%eax
  4618d0: 89 45 f0                     	movl	%eax, -0x10(%ebp)
  4618d3: c7 45 fc 00 00 00 00         	movl	$0x0, -0x4(%ebp)
  4618da: 8d 55 b4                     	leal	-0x4c(%ebp), %edx
  4618dd: 8b 45 fc                     	movl	-0x4(%ebp), %eax
  4618e0: 40                           	incl	%eax
  4618e1: e8 ea 64 fa ff               	calll	0x407dd0 <CODE+0x6dd0>
  4618e6: 8b 4d b4                     	movl	-0x4c(%ebp), %ecx
  4618e9: 8d 45 b8                     	leal	-0x48(%ebp), %eax
  4618ec: ba 74 1a 46 00               	movl	$0x461a74, %edx         # imm = 0x461A74
  4618f1: e8 ca 28 fa ff               	calll	0x4041c0 <CODE+0x31c0>
  4618f6: 8b 45 b8                     	movl	-0x48(%ebp), %eax
  4618f9: 50                           	pushl	%eax
  4618fa: 8b 0d 14 5c 46 00            	movl	0x465c14, %ecx
  461900: 83 c1 03                     	addl	$0x3, %ecx
  461903: 0f af 4d fc                  	imull	-0x4(%ebp), %ecx
  461907: 8b 87 28 03 00 00            	movl	0x328(%edi), %eax
  46190d: 33 d2                        	xorl	%edx, %edx
  46190f: e8 d0 e3 ff ff               	calll	0x45fce4 <CODE+0x5ece4>
  461914: a1 14 5c 46 00               	movl	0x465c14, %eax
  461919: 85 c0                        	testl	%eax, %eax
  46191b: 7c 7d                        	jl	0x46199a <CODE+0x6099a>
  46191d: 40                           	incl	%eax
  46191e: 89 45 ec                     	movl	%eax, -0x14(%ebp)
  461921: 33 f6                        	xorl	%esi, %esi
  461923: a1 2c 5c 46 00               	movl	0x465c2c, %eax
  461928: 8b 55 fc                     	movl	-0x4(%ebp), %edx
  46192b: 8b 04 90                     	movl	(%eax,%edx,4), %eax
  46192e: 8b 04 b0                     	movl	(%eax,%esi,4), %eax
  461931: 8d 55 b0                     	leal	-0x50(%ebp), %edx
  461934: e8 97 64 fa ff               	calll	0x407dd0 <CODE+0x6dd0>
  461939: 8b 45 b0                     	movl	-0x50(%ebp), %eax
  46193c: 50                           	pushl	%eax
  46193d: 8b 0d 14 5c 46 00            	movl	0x465c14, %ecx
  461943: 83 c1 03                     	addl	$0x3, %ecx
  461946: 0f af 4d fc                  	imull	-0x4(%ebp), %ecx
  46194a: 03 ce                        	addl	%esi, %ecx
  46194c: 41                           	incl	%ecx
  46194d: 8b 87 28 03 00 00            	movl	0x328(%edi), %eax
  461953: 33 d2                        	xorl	%edx, %edx
  461955: e8 8a e3 ff ff               	calll	0x45fce4 <CODE+0x5ece4>
  46195a: a1 30 5c 46 00               	movl	0x465c30, %eax
  46195f: 8b 55 fc                     	movl	-0x4(%ebp), %edx
  461962: 8b 04 90                     	movl	(%eax,%edx,4), %eax
  461965: 8b 04 b0                     	movl	(%eax,%esi,4), %eax
  461968: 8d 55 ac                     	leal	-0x54(%ebp), %edx
  46196b: e8 60 64 fa ff               	calll	0x407dd0 <CODE+0x6dd0>
  461970: 8b 45 ac                     	movl	-0x54(%ebp), %eax
  461973: 50                           	pushl	%eax
  461974: 8b 0d 14 5c 46 00            	movl	0x465c14, %ecx
  46197a: 83 c1 03                     	addl	$0x3, %ecx
  46197d: 0f af 4d fc                  	imull	-0x4(%ebp), %ecx
  461981: 03 ce                        	addl	%esi, %ecx
  461983: 41                           	incl	%ecx
  461984: 8b 87 28 03 00 00            	movl	0x328(%edi), %eax
  46198a: ba 01 00 00 00               	movl	$0x1, %edx
  46198f: e8 50 e3 ff ff               	calll	0x45fce4 <CODE+0x5ece4>
  461994: 46                           	incl	%esi
  461995: ff 4d ec                     	decl	-0x14(%ebp)
  461998: 75 89                        	jne	0x461923 <CODE+0x60923>
  46199a: ff 45 fc                     	incl	-0x4(%ebp)
  46199d: ff 4d f0                     	decl	-0x10(%ebp)
  4619a0: 0f 85 34 ff ff ff            	jne	0x4618da <CODE+0x608da>
  4619a6: 33 c0                        	xorl	%eax, %eax
  4619a8: 5a                           	popl	%edx
  4619a9: 59                           	popl	%ecx
  4619aa: 59                           	popl	%ecx
  4619ab: 64 89 10                     	movl	%edx, %fs:(%eax)
  4619ae: 68 d6 19 46 00               	pushl	$0x4619d6               # imm = 0x4619D6
  4619b3: 8d 45 ac                     	leal	-0x54(%ebp), %eax
  4619b6: ba 0f 00 00 00               	movl	$0xf, %edx
  4619bb: e8 18 25 fa ff               	calll	0x403ed8 <CODE+0x2ed8>
  4619c0: 8d 45 f8                     	leal	-0x8(%ebp), %eax
  4619c3: 8b 15 5c 13 46 00            	movl	0x46135c, %edx
  4619c9: e8 d2 34 fa ff               	calll	0x404ea0 <CODE+0x3ea0>
  4619ce: c3                           	retl
  4619cf: e9 e4 1e fa ff               	jmp	0x4038b8 <CODE+0x28b8>
  4619d4: eb dd                        	jmp	0x4619b3 <CODE+0x609b3>
  4619d6: 5f                           	popl	%edi
  4619d7: 5e                           	popl	%esi
  4619d8: 5b                           	popl	%ebx
  4619d9: 8b e5                        	movl	%ebp, %esp
  4619db: 5d                           	popl	%ebp
  4619dc: c3                           	retl
  4619dd: 00 00                        	addb	%al, (%eax)
  4619df: 00 ff                        	addb	%bh, %bh
  4619e1: ff ff                        	<unknown>
  4619e3: ff 0a                        	decl	(%edx)
  4619e5: 00 00                        	addb	%al, (%eax)
  4619e7: 00 cf                        	addb	%cl, %bh
  4619e9: f0                           	lock
  4619ea: e0 e2                        	loopne	0x4619ce <CODE+0x609ce>
  4619ec: e8 eb fc ed ee               	calll	0xef3416dc
