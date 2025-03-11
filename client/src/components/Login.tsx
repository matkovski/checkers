import {useState} from 'react'

export default function() {
    let [a, setA] = useState(0);

    let data = ['one', 'two', 'three']
    return (
        <>
            {data.map(v => (
                <div>and {v}!</div>
            ))}
            I am a component i suppose?
        </>
    )
}