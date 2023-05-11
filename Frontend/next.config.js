// PRODUCTION
// module.exports = () => {
//   const rewrites = () => {
//     return [
//       {
//         source: "/schedule",
//         destination: "http://172.17.0.5:8000/schedule/",
//       },
//       {
//         source: "/register",
//         destination: "http://172.17.0.5:8000/register/",
//       },
//       {
//         source: "/signin",
//         destination: "http://172.17.0.5:8000/signin/",
//       },
//       {
//         source: "/update",
//         destination: "http://172.17.0.5:8000/update/",
//       },
//       {
//         source: "/confirm",
//         destination: "http://172.17.0.5:8000/confirm/",
//       },
//     ];
//   };
//   return {
//     rewrites
//   };
// };

////////////////////////////

// DEVELOPMENT
module.exports = () => {
  const rewrites = () => {
    return [
      {
        source: "/schedule",
        destination: "http://localhost:8000/schedule/",
      },
      {
        source: "/register",
        destination: "http://localhost:8000/register/",
      },
      {
        source: "/signin",
        destination: "http://localhost:8000/signin/",
      },
      {
        source: "/update",
        destination: "http://localhost:8000/update/",
      },
      {
        source: "/confirm",
        destination: "http://localhost:8000/confirm/",
      },
    ];
  };
  return {
    rewrites
  };
};
