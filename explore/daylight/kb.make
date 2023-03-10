default:
	m4 --quiet -P kb.pre > kb.pre2
	sed  s/COMMA/,/g kb.pre2 > kb.js
