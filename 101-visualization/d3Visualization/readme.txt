index1和index2都是表示图的。
index1可以将节点分为不同group，并根据不同节点之间的value大小确定线的粗细。
我们把所有人放同一组即可。完美符合要求。
index2不把节点分为不同group，只要简单定义点之间的连接，但是不通过直接定义的value来确定线的粗细。
而是判断节点之间属性相似度来确定节点之间的联结强度。我们可以把一位选手的所有关键词（或者高频）的词向量（百度NLP里也有）作为她的属性。
								^
								^
								^
mission:process wordleFInalresult(all).json. Get vector data.
format:{
	result:[{name:"", value:[1.0,2.3,4.3,2.0...]}, {}, {}...]
}