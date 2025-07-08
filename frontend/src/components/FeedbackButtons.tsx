export default function FeedbackButtons({ selected }: { selected: string }) {
  const send = (good: boolean) => {
    fetch('/feedback/', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({user_query:selected, q1_list:[selected], selected_q2: good ? selected : null, topk:1})})
  }
  return (
    <div>
      <button onClick={()=>send(true)}>👍</button>
      <button onClick={()=>send(false)}>👎</button>
    </div>
  )
}
