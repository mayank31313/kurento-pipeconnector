#include "PipeConnector.hpp"
#include "base64.h"
#include <iostream>

using namespace std;

namespace ior{
	std::string encode(cv::Mat &img){
		std::vector<uchar> buf;
		cv::imencode(".jpg", img, buf);
		auto *enc_msg = reinterpret_cast<unsigned char*>(buf.data());
		return base64_encode(enc_msg, buf.size());
	}

	cv::Mat decode(std::string &image){
		std:string dec_jpg = base64_decode(image);
		std::vector<uchar> data(dec_jpg.begin(), dec_jpg.end());
		return cv::imdecode(cv::Mat(data), 1);
	}

	PipeConnector::PipeConnector(){
		PipeConnector::socket = zmq::socket_t(PipeConnector::ctx, zmq::socket_type::req);
	}

	void PipeConnector::connectServer(const std::string &server){
		PipeConnector::addProperty("server", server);

		PipeConnector::socket.connect(server);
		PipeConnector::sendMessage("1");
		PipeConnector::clientToken.clear();
		PipeConnector::receiveMessage(PipeConnector::clientToken);
	}

	void PipeConnector::disconnectServer(){

	}

	void PipeConnector::addProperty(const std::string &name, const std::string &value){
		struct KeyValue pair;
		pair.key = name;
		pair.value = value;

		PipeConnector::properties.push_back(pair);
	}

	void PipeConnector::sendMessage(const std::string &message){
		zmq::const_buffer buffer(message.c_str(), message.length());
		PipeConnector::send_msgs.clear();
		PipeConnector::send_msgs.push_back(zmq::const_buffer(clientToken.c_str(), clientToken.length()));
		PipeConnector::send_msgs.push_back(buffer);

		try{
			zmq::send_multipart(PipeConnector::socket, PipeConnector::send_msgs);
		}catch(zmq::error_t error){
			cout<<"Error"<<error.what()<<endl;
		}
	}

	std::string PipeConnector::findPropertyByKey(std::string &name){
		std::vector<KeyValue>::iterator  iterator;
		for(iterator = properties.begin(); iterator != properties.end(); ++iterator){
			if(iterator->key == name){
				return iterator->value;
			}
		}
		return "";
	}

	void PipeConnector::send_image(cv::Mat &mat){
		std::string encoded = encode(mat);
		PipeConnector::encodedImage.clear();
		PipeConnector::encodedImage.append(encoded);
		PipeConnector::sendMessage(PipeConnector::encodedImage);
	}

	void PipeConnector::receiveMessage(std::string &message){
		recv_msgs.clear();
		const auto ret = zmq::recv_multipart(PipeConnector::socket, std::back_inserter(recv_msgs));
		for(int i=0;i<recv_msgs.size();i++){
			message.append(recv_msgs[i].to_string());
		}
	}

	cv::Mat PipeConnector::receiveImage(){
		encodedImage.clear();
		receiveMessage(encodedImage);
		cv::Mat dst = decode(encodedImage);
		return dst;
	}
}
