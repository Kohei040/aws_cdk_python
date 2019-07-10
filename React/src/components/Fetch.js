import React from 'react';
import 'whatwg-fetch';

// class Fetch extends React.Component {
//   constructor(prps) {
//     super(props);
//     this.state = {
//       error: null,
//       isLoaded: false,
//       items: []
//     };
//   }
//
//   componentDidMount() {
//     fetch("https://api.example.com/items")
//     .then(res => res.json())
//     .then(
//       (result) => {
//         this.setState({
//           isLoaded: true,
//           items: result.items
//         });
//       },
//       (error) => {
//         this.setState({
//           isLoaded: true,
//           error
//         });
//       }
//     )
//   }
//
//   render() {
//     const { error, isLoaded, items } = this.state;
//     if (error) {
//       return <div>Error: {error.message}</div>;
//     } else if (!isLoaded) {
//       return <div>Loading...</div>;
//     } else {
//       return (
//         <ul>
//           {items.map(item => (
//             <li key={item.name}>
//               {item.naem} {item.price}
//             </li>
//           ))}
//         </ul>
//       );
//     }
//   }
// }

export default function Fetch() {
  fetch('https://httpbin.org/ip')
    .then(response => {
      // const json = "test"
      // return(json);
      console.log(JSON.stringify(response));
  });
  return response
}
