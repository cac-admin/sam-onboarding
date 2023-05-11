sudo docker stop tb-backend
sudo docker rm tb-backend

sudo docker stop tb-frontend
sudo docker rm tb-backend

cd /home/opc/sam-onboarding
git pull
cd Backend
sudo docker build -t tb-backend .
cd ../Frontend
sudo docker build -t tb-frontend .

sudo docker run -d -p 8000:8000 --name tb-backend tb-backend
sudo docker run -d -p 3000:3000 --name tb-frontend tb-frontend
echo "Reload Complete"