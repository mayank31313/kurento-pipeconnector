#include <zmq_addon.hpp>
#include <opencv2/opencv.hpp>

namespace ior{
	struct Layer{
		std::string id;
		std::string name;
	};
	struct KeyValue{
		std::string key;
		std::string value;
	};

	std::string encode(cv::Mat &img);
	cv::Mat decode(std::string &img);

	class PipeConnector{
	public:
		PipeConnector();
		void connectServer(const std::string &server);
		void disconnectServer();
		void send_image(cv::Mat &mat);
		cv::Mat receiveImage();
		void addProperty(const std::string &name, const std::string &value);
		void terminate();
	protected:
		std::string findPropertyByKey(std::string &name);
	private:
		std::vector<Layer> layers;
		std::string clientToken;
		zmq::context_t ctx;
		zmq::socket_t socket;
		std::vector<KeyValue> properties;
		std::vector<zmq::const_buffer> send_msgs;
		std::vector<zmq::message_t> recv_msgs;
		void sendMessage(const std::string &message);
		void receiveMessage(std::string &message);
		std::string encodedImage = "";
	};
}
