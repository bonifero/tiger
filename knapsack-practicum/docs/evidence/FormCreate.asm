
/Users/cassidal/Documents/vuz/tiger/source/Лаб_3/Загрузка_рюкзака.exe:	file format coff-i386

Disassembly of section CODE:

00401000 <CODE>:
  460288: ba a8 02 46 00               	movl	$0x4602a8, %edx         # imm = 0x4602A8
  46028d: 8b 80 14 03 00 00            	movl	0x314(%eax), %eax
  460293: e8 18 32 fd ff               	calll	0x4334b0 <CODE+0x324b0>
  460298: 33 c0                        	xorl	%eax, %eax
  46029a: a3 40 5c 46 00               	movl	%eax, 0x465c40
  46029f: c3                           	retl
