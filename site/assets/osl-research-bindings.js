(function(root,factory){if(typeof module==='object'&&module.exports)module.exports=factory;else root.Omega42Operations=factory(root.Omega42Suite)})(typeof self!=='undefined'?self:this,function(M){
'use strict';
const integer=(x,min,max)=>{if(!Number.isSafeInteger(x)||x<min||x>max)throw RangeError('Expected integer '+min+'..'+max);return x};
const depth=(x,max=4)=>integer(x,1,max);
const phases=(a,k)=>{if(!Array.isArray(a)||a.length>32)throw Error('Expected at most 32 phases');return a.map(t=>integer(t,0,M.order(k)-1))};
const ops=Object.freeze({
'OBS.PARTITION':{basis:'MF-201/207/208',run:(k,t)=>M.partition(phases(t,depth(k,6)),k)},
'OBS.DESCEND':{basis:'MF-214',run:(k,t)=>M.descend(phases(t,depth(k,6)),k)},
'OBS.COMPLETE':{basis:'MF-221',run:(k,t,p)=>M.complete(phases(t,depth(k)),k,phases(p,k))},
'MEM.INVARIANT':{basis:'MF-220',run:(k,s)=>M.invariant(integer(s,0,3**depth(k,12)-1),k)},
'MEM.EXTINCTION':{basis:'MF-220',run:(k,w)=>M.extinctionDepth(integer(w,0,3**depth(k,12)-1),k)},
'MEM.LIFT':{basis:'MF-220',run:(k,w,s,j)=>{depth(k,12);integer(w,0,3**k-1);integer(s,0,3**k-1);integer(j,0,33-k);return M.trajectory(w,s,k,j)}},
'DESIGN.RING':{basis:'MF-219',run:k=>M.verifyDesign(depth(k,3))},
'GEN.DISTANCE':{basis:'MF-209–212',run:(k,o,a,b)=>{depth(k,5);if(typeof o!=='string'||! /^(?!.*(.).*\1)[AVCS]{1,4}$/.test(o))throw Error('Expected distinct AVCS operators');integer(a,0,3**k-1);integer(b,0,3**k-1);const r=M.navigate(o,k,[a,b]);return {...r,distance:r.route===null?null:r.route.length}}},
'GEN.MINSET':{basis:'MF-209–212',run:k=>{const r=M.compareSets(depth(k,4)).filter(x=>x.generates);const n=Math.min(...r.map(x=>x.ops.length));return r.filter(x=>x.ops.length===n)}},
'ADAPT.DEFECT':{basis:'Lexicon 127',run:(n,m)=>M.defect(integer(n,1,10000),integer(m,1,10000))},
'ADAPT.COMPOSE':{basis:'Lexicon 127–128',run:(n,m,l)=>M.compose(integer(n,1,10000),integer(m,1,10000),integer(l,1,10000))}
});
const arity=[2,2,3,2,2,4,1,4,1,2,3];const names=Object.keys(ops);
function execute(command){if(typeof command!=='string'||command.length>4096)throw Error('Command length limit');const match=/^([A-Z]+\.[A-Z]+)\s+(\[.*\])$/s.exec(command.trim());if(!match||!Object.hasOwn(ops,match[1]))throw Error('Unknown operation; use NAME [JSON arguments]');const args=JSON.parse(match[2]);if(!Array.isArray(args)||args.length!==arity[names.indexOf(match[1])])throw Error('Incorrect argument count');const op=ops[match[1]];return {protocol:'OmegaSL research bindings proposal v1',kernel:M.VERSION,operation:match[1],arguments:args,basis:op.basis,status:'EXECUTED',result:op.run(...args)}}
return {execute,names};
});