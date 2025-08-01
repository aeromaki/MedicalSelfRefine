`ps -ef | grep multiprocessing`.split("\n").map{|x| x.split()[1] }.each{|x| `kill -9 #{x}`}
