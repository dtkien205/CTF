(()=>{const f=document.createElement('form');f.method='POST';f.action='/create_game';
const a=document.createElement('input');a.name='language';a.value='/flag';    // <-- quan trọng
const b=document.createElement('input');b.name='hard_mode';b.value='on';      // có/không đều được
f.append(a,b);document.body.appendChild(f);f.submit();})();
