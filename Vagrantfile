Vagrant.configure("2") do |config|
  # See documentation for more configuration options.
  # https://docs.vagrantup.com.

  config.vm.box = "hashicorp/bionic64"

  
  config.vm.network "forwarded_port", guest: 5000, host: 5000

  config.vm.provision "shell", privileged: false, inline: <<-SHELL    
    sudo apt-get update    
    sudo apt-get install -y build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
xz-utils tk-dev libffi-dev liblzma-dev python-openssl git 
    git clone https://github.com/pyenv/pyenv.git ~/.pyenv
    cd ~/.pyenv && src/configure && make -C src
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.profile
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.profile
    echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.profile
    source ~/.profile
    pyenv install 3.9.1
    pyenv global 3.9.1
 
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

    cd /vagrant && poetry install

  SHELL

  config.trigger.after :up do |trigger|    
    trigger.name = "Launching App"    
    trigger.info = "Running the TODO app setup script"    
    trigger.run_remote = {privileged: false, inline: "      

    # can run application with either poetry or gunicorn, uncomment poetry and comment gunicorn if you want to switch
    #nohup poetry run flask run --host 0.0.0.0 > logs.txt 2>&1 & 
    export `cat .env | grep '^[A-Z]' | xargs` # export the .env file in to environment variables that gunicorn can use
    poetry run gunicorn --daemon -b 0.0.0.0:5000 todo_app.wsgi:wsgi_app --log-file gunicorn_logs.txt
    "}
  end

end
