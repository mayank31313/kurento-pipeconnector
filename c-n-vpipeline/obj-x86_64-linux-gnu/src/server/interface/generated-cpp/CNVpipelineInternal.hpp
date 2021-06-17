/* Autogenerated with kurento-module-creator */

#ifndef __CNVPIPELINE_INTERNAL_HPP__
#define __CNVPIPELINE_INTERNAL_HPP__

#include "CNVpipeline.hpp"

namespace kurento
{
class JsonSerializer;
}

namespace kurento
{
class MediaPipeline;
} /* kurento */

namespace kurento
{
namespace module
{
namespace cnvpipeline
{

class CNVpipelineMethodConnectServer
{
public:
  CNVpipelineMethodConnectServer() = default;
  ~CNVpipelineMethodConnectServer() = default;

  void invoke (std::shared_ptr<CNVpipeline> obj);
  void Serialize (JsonSerializer &serializer);

  std::string getServer () {
    return server;
  }

  void setServer (const std::string &server) {
    this->server = server;
  }

private:
  std::string server;
};

class CNVpipelineMethodSetToken
{
public:
  CNVpipelineMethodSetToken() = default;
  ~CNVpipelineMethodSetToken() = default;

  void invoke (std::shared_ptr<CNVpipeline> obj);
  void Serialize (JsonSerializer &serializer);

  std::string getToken () {
    return token;
  }

  void setToken (const std::string &token) {
    this->token = token;
  }

private:
  std::string token;
};

class CNVpipelineMethodDisconnectServer
{
public:
  CNVpipelineMethodDisconnectServer() = default;
  ~CNVpipelineMethodDisconnectServer() = default;

  void invoke (std::shared_ptr<CNVpipeline> obj);
  void Serialize (JsonSerializer &serializer);

};

class CNVpipelineMethodAddProperty
{
public:
  CNVpipelineMethodAddProperty() = default;
  ~CNVpipelineMethodAddProperty() = default;

  void invoke (std::shared_ptr<CNVpipeline> obj);
  void Serialize (JsonSerializer &serializer);

  std::string getName () {
    return name;
  }

  void setName (const std::string &name) {
    this->name = name;
  }

  std::string getValue () {
    return value;
  }

  void setValue (const std::string &value) {
    this->value = value;
  }

private:
  std::string name;
  std::string value;
};

class CNVpipelineMethodSetId
{
public:
  CNVpipelineMethodSetId() = default;
  ~CNVpipelineMethodSetId() = default;

  void invoke (std::shared_ptr<CNVpipeline> obj);
  void Serialize (JsonSerializer &serializer);

  std::string getId () {
    return id;
  }

  void setId (const std::string &id) {
    this->id = id;
  }

private:
  std::string id;
};

class CNVpipelineConstructor
{
public:
  CNVpipelineConstructor() = default;
  ~CNVpipelineConstructor() = default;

  void Serialize (JsonSerializer &serializer);

  std::shared_ptr<MediaPipeline> getMediaPipeline ();

  void setMediaPipeline (std::shared_ptr<MediaPipeline> mediaPipeline) {
    this->mediaPipeline = mediaPipeline;
  }

private:
  std::shared_ptr<MediaPipeline> mediaPipeline;
};

} /* cnvpipeline */
} /* module */
} /* kurento */

#endif /*  __CNVPIPELINE_INTERNAL_HPP__ */
