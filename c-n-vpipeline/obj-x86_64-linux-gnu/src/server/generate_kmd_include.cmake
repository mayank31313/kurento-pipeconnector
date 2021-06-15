  execute_process (COMMAND /usr/bin/kurento-module-creator -r /home/klaus/Desktop/kurento-plugins/PipeConnector/c-n-vpipeline/src/server/interface ;-dr;/usr/share/kurento/modules -o /home/klaus/Desktop/kurento-plugins/PipeConnector/c-n-vpipeline/obj-x86_64-linux-gnu/src/server/)

  file (READ /home/klaus/Desktop/kurento-plugins/PipeConnector/c-n-vpipeline/obj-x86_64-linux-gnu/src/server/cnvpipeline.kmd.json KMD_DATA)

  string (REGEX REPLACE "\n *" "" KMD_DATA ${KMD_DATA})
  string (REPLACE "\"" "\\\"" KMD_DATA ${KMD_DATA})
  string (REPLACE "\\n" "\\\\n" KMD_DATA ${KMD_DATA})
  set (KMD_DATA "\"${KMD_DATA}\"")

  file (WRITE /home/klaus/Desktop/kurento-plugins/PipeConnector/c-n-vpipeline/obj-x86_64-linux-gnu/src/server/cnvpipeline.kmd.json ${KMD_DATA})
