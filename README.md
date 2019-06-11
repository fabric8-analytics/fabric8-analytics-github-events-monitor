# Github monitoring service

 * takes a list of golang package names
 * map the names from the list to Github repositories (skip everyting else)
 * periodically scan events, that occured in the repositories
 * send notifications to the specified backend