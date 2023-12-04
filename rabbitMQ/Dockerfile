FROM rabbitmq:management

# Define environment variables.
ENV RABBITMQ_DEFAULT_USER user
ENV RABBITMQ_DEFAULT_PASS password

ADD entrypoint.sh /entrypoint.sh

RUN ["chmod", "+x", "/entrypoint.sh"]

EXPOSE 15672

# Define default command
CMD ["/entrypoint.sh"]