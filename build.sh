#!/bin/bash
FOLDER="c-n-vpipeline"

rm *.deb
rm *.ddeb

(
cd ./$FOLDER/build &&
cmake .. -DGENERATE_JAVA_CLIENT_PROJECT=TRUE &&
make
)

(cd ./$FOLDER
dpkg-buildpackage -rfakeroot -us -uc -b && \ 
docker build -t mayank31313/kurento-additionalmodules .. &&
docker run --rm mayank31313/kurento-additionalmodules --version
)

cp -r ./$FOLDER/build/java/* ./java/
