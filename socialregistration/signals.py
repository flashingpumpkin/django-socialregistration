from django import dispatch

login = dispatch.Signal(providing_args = ["user", "profile", "client"])
connect = dispatch.Signal(providing_args = ["user", "profile", "client"])
