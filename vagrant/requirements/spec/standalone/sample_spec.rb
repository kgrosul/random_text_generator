require 'spec_helper'


describe package('python3-pip')  do
  it { should be_installed }
end

describe package('python3-venv')  do
  it { should be_installed }
end

describe package('python3')  do
  it { should be_installed }
end

describe command('python3.6 --version') do
  its(:stdout) { should contain('3.6') }
end

describe host_inventory['memory']['total'].delete('kB').to_i do 
  it { should > 490000 }
end


describe host_inventory['cpu']['total'].to_i do 
  it { should > 0 }
end


