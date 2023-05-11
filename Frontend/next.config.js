
module.exports = {
	async rewrites() { 
	return [
      {
        source: "/schedule",
        destination: "http://127.0.0.1:8000/schedule/",
      },
      {
        source: "/register",
        destination: "http://127.0.0.1:8000/register/",
      },
      {
        source: "/signin",
        destination: "http://127.0.0.1:8000/signin/",
      },
      {
        source: "/update",
        destination: "http://127.0.0.1:8000/update/",
      },
      {
        source: "/confirm",
        destination: "http://127.0.0.1:8000/confirm/",
      },
    ];
},
};

module.exports.output = 'standalone';
