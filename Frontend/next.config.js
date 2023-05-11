
// module.exports = {
// 	async rewrites() { 
// 	return [
//       {
//         source: "/schedule",
//         destination: "http://172.17.0.2:8000/schedule/",
//       },
//       {
//         source: "/register",
//         destination: "http://172.17.0.2:8000/register/",
//       },
//       {
//         source: "/signin",
//         destination: "http://172.17.0.2:8000/signin/",
//       },
//       {
//         source: "/update",
//         destination: "http://172.17.0.2:8000/update/",
//       },
//       {
//         source: "/confirm",
//         destination: "http://172.17.0.2:8000/confirm/",
//       },
//     ];
// },
// };

module.exports = () => {
  const rewrites = () => {
    return [
      {
        source: "/schedule",
        destination: "http://172.17.0.5:8000/schedule/",
      },
      {
        source: "/register",
        destination: "http://172.17.0.5:8000/register/",
      },
      {
        source: "/signin",
        destination: "http://172.17.0.5:8000/signin/",
      },
      {
        source: "/update",
        destination: "http://172.17.0.5:8000/update/",
      },
      {
        source: "/confirm",
        destination: "http://172.17.0.5:8000/confirm/",
      },
    ];
  };
  return {
    rewrites
  };
};

// module.exports.output = 'standalone';
